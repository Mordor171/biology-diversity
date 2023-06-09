<template>
  <PageWrapper dense contentFullHeight fixedHeight contentClass="flex">
    <!--    <DeptTree class="w-1/4 xl:w-1/5" @select="handleSelect" />-->
    <BasicTable @register="registerTable" class="" :searchInfo="searchInfo">
      <template #tableTitle>
        <Space style="height: 40px">
          <a-button
            type="primary"
            v-auth="['post:add']"
            preIcon="ant-design:plus-outlined"
            @click="handleCreate"
          >
            新增
          </a-button>

          <a-button
            type="error"
            v-auth="['post:delete']"
            preIcon="ant-design:delete-outlined"
            @click="handleBulkDelete"
          >
            删除
          </a-button>
        </Space>
      </template>
      <template #action="{ record }">
        <TableAction
          :actions="[
            {
              type: 'button',
              icon: 'clarity:note-edit-line',
              color: 'primary',
              auth: ['user:update'],
              disabled: record.id === 1,
              onClick: handleEdit.bind(null, record),
            },
            {
              icon: 'ant-design:delete-outlined',
              type: 'button',
              color: 'error',
              placement: 'left',
              auth: ['user:delete'],
              disabled: record.id === 1,
              popConfirm: {
                title: '是否确认删除',
                confirm: handleDelete.bind(null, record.id),
              },
            },
          ]"
        />
      </template>
    </BasicTable>
    <AccountModal @register="registerDrawer" @success="handleSuccess" />
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, reactive } from 'vue';

  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { PageWrapper } from '/@/components/Page';

  import { useDrawer } from '/@/components/Drawer';
  import AccountModal from './AccountDrawer.vue';

  import { columns, searchFormSchema } from './account.data';
  import { useGo } from '/@/hooks/web/usePage';
  import { getList, deleteItem } from './account.api';
  import { message, Space } from 'ant-design-vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  export default defineComponent({
    name: 'AccountManagement',
    components: { BasicTable, PageWrapper, AccountModal, TableAction, Space },
    setup() {
      const go = useGo();
      const [registerDrawer, { openDrawer }] = useDrawer();
      const { createConfirm } = useMessage();
      const searchInfo = reactive<Recordable>({});
      const [registerTable, { reload, updateTableDataRecord, getSelectRows }] = useTable({
        api: getList,
        rowKey: 'id',
        columns,
        formConfig: {
          labelWidth: 80,
          schemas: searchFormSchema,
          autoSubmitOnEnter: true,
        },
        useSearchForm: true,
        tableSetting: { fullScreen: true },
        showTableSetting: true,
        bordered: true,
        handleSearchInfoFn(info) {
          // console.log('handleSearchInfoFn', info);
          return info;
        },
        rowSelection: {
          type: 'checkbox',
          getCheckboxProps(record: Recordable) {
            // Demo: 第一行（id为0）的选择框禁用
            if (record.id === 1) {
              return { disabled: true };
            } else {
              return { disabled: false };
            }
          },
        },
        actionColumn: {
          width: 120,
          title: '操作',
          dataIndex: 'action',
          slots: { customRender: 'action' },
        },
      });

      function handleCreate() {
        openDrawer(true, {
          isUpdate: false,
        });
      }

      function handleEdit(record: Recordable) {
        // console.log(record);
        openDrawer(true, {
          record,
          isUpdate: true,
        });
      }

      async function handleDelete(id: number) {
        await deleteItem(id);
        await reload();
      }

      function handleBulkDelete() {
        if (getSelectRows().length == 0) {
          message.warning('请选择一个选项');
        } else {
          createConfirm({
            iconType: 'warning',
            title: '提示',
            content: '是否确认删除？',
            async onOk() {
              for (const item of getSelectRows()) {
                await deleteItem(item.id);
              }
              message.success('删除成功');
              await reload();
            },
          });
        }
      }

      function handleSuccess({ isUpdate, values }) {
        if (isUpdate) {
          // 演示不刷新表格直接更新内部数据。
          // 注意：updateTableDataRecord要求表格的rowKey属性为string并且存在于每一行的record的keys中
          const result = updateTableDataRecord(values.id, values);
          // console.log(result);
        } else {
          reload();
        }
      }

      function handleSelect(deptId = '') {
        searchInfo.deptId = deptId;
        reload();
      }

      function handleView(record: Recordable) {
        go('/system/account_detail/' + record.id);
      }

      return {
        registerTable,
        registerDrawer,
        handleCreate,
        handleEdit,
        handleDelete,
        handleSuccess,
        handleSelect,
        handleView,
        searchInfo,
        handleBulkDelete,
      };
    },
  });
</script>
