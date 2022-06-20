<template>
  <PageWrapper contentClass="flex">
    <BasicTable @register="registerTable">
      <template #tableTitle>
        <InputSearch
          v-model:value="searchText"
          placeholder="模糊搜索"
          style="width: 300px"
          @search="onSearch"
          allow-clear
        />
      </template>
      <template #toolbar>
        <a-button type="primary" @click="handleCreate"> 新建组织 </a-button>
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
              color: 'error',
              popConfirm: {
                title: '是否确认删除',
                confirm: handleDelete.bind(null, record),
                placement: 'topRight',
              },
            },
          ]"
        />
      </template>
    </BasicTable>
    <OrgEditor @register="registerDrawer" @success="handleSuccess" />
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { InputSearch, notification } from 'ant-design-vue';
  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { useDrawer } from '/@/components/Drawer';
  import OrgEditor from './OrgEditor.vue';
  import { columns } from './organization.data';
  import {
    apiDeleteOrganizationItem,
    apiGetOrganizationList,
  } from '/@/api/system-config/ortanization';
  import { PageWrapper } from '/@/components/Page';
  export default defineComponent({
    name: 'OrganizationManagement',
    components: { PageWrapper, BasicTable, OrgEditor, TableAction, InputSearch },
    setup() {
      const searchText = ref('');
      const [registerDrawer, { openDrawer }] = useDrawer();
      const [registerTable, { reload }] = useTable({
        api: async (params) => {
          const res = await apiGetOrganizationList({
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
        apiDeleteOrganizationItem(record.id).then((res) => {
          if (res.code == 200) {
            console.log('Delete org: ' + record.id);
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
