<template>
  <PageWrapper contentClass="flex">
    <BasicTable @register="registerTable" @fetch-success="onFetchSuccess">
      <template #toolbar>
        <a-button type="primary" @click="handleCreate"> 新建菜单 </a-button>
      </template>
      <template #action="{ record }">
        <TableAction
          :actions="[
            {
              icon: 'clarity:note-edit-line',
              onClick: handleEdit.bind(null, record),
            },
            {
              icon: 'healthicons:database-outline',
              color: 'warning',
              onClick: handleDataPermissionEdit.bind(null, record),
            },
            {
              icon: 'ant-design:delete-outlined',
              color: 'error',
              popConfirm: {
                title: '将同时删除子节点，是否确认删除',
                confirm: handleDelete.bind(null, record),
                placement: 'topRight',
              },
            },
          ]"
        />
      </template>
    </BasicTable>
    <MenuEditor @register="registerEditDrawer" @success="handleSuccess" />
    <RouteSelector @register="registerRouteSelectDrawer" @success="handleSuccess" />
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, nextTick } from 'vue';
  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { PageWrapper } from '/@/components/Page';
  import { useDrawer } from '/@/components/Drawer';
  import { apiDeleteMenuItem, getMenuListForManager } from '/@/api/system-config/menu';
  import MenuEditor from './MenuEditor.vue';
  import RouteSelector from './RouteSelector.vue';
  import { columns } from './menu.data';
  import { notification } from 'ant-design-vue';
  export default defineComponent({
    name: 'MenuManagement',
    components: { PageWrapper, BasicTable, MenuEditor, RouteSelector, TableAction },
    setup() {
      const [registerEditDrawer, { openDrawer: openEditDrawer }] = useDrawer();
      const [registerRouteSelectDrawer, { openDrawer: openRouteSelectDrawer }] = useDrawer();

      const [registerTable, { reload, expandAll }] = useTable({
        // title: '菜单列表',
        api: getMenuListForManager,
        columns,
        isTreeTable: true,
        pagination: false,
        striped: false,
        showTableSetting: false,
        bordered: true,
        showIndexColumn: false,
        canResize: false,
        actionColumn: {
          width: 140,
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
      function handleDataPermissionEdit(record: Recordable) {
        openRouteSelectDrawer(true, {
          menu_id: record.id,
          menu_title: record.title,
        });
      }
      function handleDelete(record: Recordable) {
        apiDeleteMenuItem(record.id).then((res) => {
          if (res.code == 200) {
            console.log('Delete menu: ' + record.id);
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
      function onFetchSuccess() {
        // 演示默认展开所有表项
        nextTick(expandAll);
      }
      return {
        registerTable,
        registerEditDrawer,
        registerRouteSelectDrawer,
        handleCreate,
        handleEdit,
        handleDataPermissionEdit,
        handleDelete,
        handleSuccess,
        onFetchSuccess,
      };
    },
  });
</script>
