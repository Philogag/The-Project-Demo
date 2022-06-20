<template>
  <PageWrapper contentClass="flex">
    <BasicTable @register="registerTable">
      <template #toolbar>
        <a-button type="primary" @click="handleCreate"> 新建角色 </a-button>
      </template>
      <template #action="{ record }">
        <TableAction
          :actions="[
            {
              icon: 'clarity:note-edit-line',
              onClick: handleEdit.bind(null, record),
              ifShow: () => {
                return record.editable;
              },
            },
            {
              icon: 'gala:menu-left',
              color: 'warning',
              onClick: handleEditMenu.bind(null, record.id),
            },
            {
              icon: 'ant-design:delete-outlined',
              color: 'error',
              ifShow: () => {
                return record.editable;
              },
              popConfirm: {
                title: '是否确认删除',
                confirm: handleDelete.bind(null, record.id),
                placement: 'topRight',
              },
            },
          ]"
        />
      </template>
    </BasicTable>
    <RoleEditor @register="registerEditDrawer" @success="handleSuccess" />
    <MenuSelector @register="registerMenuDrawer" />
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent } from 'vue';
  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { useDrawer } from '/@/components/Drawer';
  import { PageWrapper } from '/@/components/Page';
  import { apiDeleteRoleItem, apiGetRoleList } from '/@/api/system-config/role';
  import RoleEditor from './RoleEditor.vue';
  import MenuSelector from './MenuSelector.vue';
  import { columns } from './role.data';
  import { notification } from 'ant-design-vue';
  export default defineComponent({
    name: 'RoleManagement',
    components: { PageWrapper, BasicTable, RoleEditor, MenuSelector, TableAction },
    setup() {
      const [registerEditDrawer, { openDrawer: openEditDrawer }] = useDrawer();
      const [registerMenuDrawer, { openDrawer: openMenuDrawer }] = useDrawer();
      const [registerTable, { reload }] = useTable({
        // title: '角色列表',
        api: apiGetRoleList,
        columns,
        striped: false,
        showTableSetting: false,
        pagination: false,
        bordered: true,
        showIndexColumn: false,
        canResize: false,
        actionColumn: {
          width: 120,
          title: '操作',
          dataIndex: 'action',
          slots: { customRender: 'action' },
          fixed: undefined,
        },
      });
      function handleCreate() {
        openEditDrawer(true, {
          isUpdate: false,
        });
      }
      function handleEdit(record: Recordable) {
        openEditDrawer(true, {
          record,
          isUpdate: true,
        });
      }
      function handleEditMenu(role_id: string) {
        openMenuDrawer(true, {
          role_id,
        });
      }
      function handleDelete(role_id: string) {
        apiDeleteRoleItem(role_id).then((res) => {
          if (res.code == 200) {
            // console.log("Delete role: " + role_id);
            reload();
          } else {
            notification.error({
              message: '错误',
              description: res.message.join('\n'),
            });
          }
        });
      }
      function handleSuccess() {
        reload();
      }
      return {
        registerTable,
        registerEditDrawer,
        registerMenuDrawer,
        handleCreate,
        handleEdit,
        handleEditMenu,
        handleDelete,
        handleSuccess,
      };
    },
  });
</script>
