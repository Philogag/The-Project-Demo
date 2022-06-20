<template>
  <PageWrapper contentClass="flex">
    <BasicTable @register="registerTable">
      <template #tableTitle>
        <InputSearch
          v-model:value="searchText"
          placeholder="模糊搜索"
          style="width: 300px"
          @search="onSearch"
          @change="onSearch"
          allow-clear
        />
      </template>
      <template #toolbar>
        <Button type="primary" @click="handleCreate"> 新建用户 </Button>
      </template>
      <template #action="{ record }">
        <TableAction
          :actions="[
            {
              icon: 'clarity:note-edit-line',
              onClick: handleEdit.bind(null, record),
            },
            {
              icon: 'ant-design:delete-outlined',
              color: 'warning',
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
    <UserEditor @register="registerDrawer" @success="handleSuccess" />
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { InputSearch, Button } from 'ant-design-vue';
  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { useDrawer } from '/@/components/Drawer';
  import { Icon } from '/@/components/Icon';
  import { PageWrapper } from '/@/components/Page';
  import { apiDeleteMasterUserById, apiGetMasterUserList } from '/@/api/system-config/master-user';
  import UserEditor from './UserEditor.vue';
  import { columns } from './user.data';
  export default defineComponent({
    name: 'UserManagement',
    components: { PageWrapper, BasicTable, UserEditor, TableAction, Icon, InputSearch, Button },
    setup() {
      const searchText = ref('');
      const [registerDrawer, { openDrawer }] = useDrawer();
      const [registerTable, { reload }] = useTable({
        api: async (params) => {
          const res = await apiGetMasterUserList({
            pageIndex: params.pageSize * (params.page - 1),
            pageSize: params.pageSize,
            searchText: searchText.value ? searchText.value : undefined,
          });
          return {
            items: res.data,
            total: res.filterCount,
          };
        },
        columns,
        isTreeTable: false,
        pagination: true,
        striped: false,
        showTableSetting: false,
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
        openDrawer(true, {
          isUpdate: false,
        });
      }
      function handleEdit(record: Recordable) {
        openDrawer(true, {
          record,
          isUpdate: true,
        });
      }
      function handleDelete(record: Recordable) {
        apiDeleteMasterUserById(record.id).then((res) => {
          if (res.code == 200) {
            // console.log("Delete master_user: " + record.id);
            reload();
          }
        });
      }
      function handleSuccess() {
        reload();
      }
      function onSearch() {
        reload();
      }
      return {
        searchText,
        registerTable,
        registerDrawer,
        handleCreate,
        handleEdit,
        handleDelete,
        handleSuccess,
        onSearch,
      };
    },
  });
</script>
