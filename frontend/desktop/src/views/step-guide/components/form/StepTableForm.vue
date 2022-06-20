<template>
  <div>
    <BasicTable @register="registerTable" :dataSource="tableData">
      <template #toolbar>
        <a-button type="primary" @click="handleCreate"> 新建 </a-button>
      </template>
      <template #action="{ record }">
        <TableAction
          v-if="!record.editable"
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
                confirm: handleDelete.bind(null, record.id),
                placement: 'topRight',
              },
            },
          ]"
        />
        <TableAction
          v-else
          :actions="[
            {
              icon: 'ant-design:check-outlined',
              onClick: handleSave.bind(null, record),
            },
            {
              icon: 'ant-design:delete-outlined',
              color: 'error',
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
  </div>
</template>
<script>
import { defineComponent, watch, ref, onMounted, toRaw } from 'vue';
import { cloneDeep, pick } from 'lodash-es';
import { BasicTable, TableAction, useTable } from '/@/components/Table';
import { buildFakeID } from '/@/utils/uuid.ts';
import { stepTableFormProps } from './props';

export default defineComponent({
  name: 'StepTableForm',
  components: {
    BasicTable,
    TableAction,
  },
  props: stepTableFormProps,
  setup(props) {
    const tableData = ref(props.data ? props.data : []);
    let pickedDataProps = [];
    let emptyData = {};
    const [registerTable, { setColumns, getDataSource, deleteTableDataRecord }] = useTable({
      columns: props.schemas ? props.schemas : [],
      rowKey: 'id',
      isTreeTable: false,
      pagination: false,
      striped: false,
      showTableSetting: false,
      bordered: true,
      showIndexColumn: false,
      canResize: true,
      actionColumn: {
        width: 120,
        title: '操作',
        dataIndex: 'action',
        slots: { customRender: 'action' },
        fixed: 'right',
      },
    });

    async function handleCreate() {
      let newData = {
        ...cloneDeep(emptyData),
        editable: true,
        id: buildFakeID(),
      };
      console.log('Create new row: ', newData);
      tableData.value.push(newData);
    }

    async function handleDelete(record_id) {
      await deleteTableDataRecord(record_id);
    }

    function handleEdit(record) {
      record.onEdit?.(true);
    }
    async function handleSave(record) {
      const validPass = await record.onValid?.();
      console.log('Valid passed: ', validPass);
      if (validPass) {
        const index = tableData.value.find((item) => item.id === record.id);
        // console.log(index);
        record.onEdit?.(false, true);
      }
    }

    function resetEmptyDataStruct(schemas) {
      emptyData = {};
      pickedDataProps = ['id', 'editable'];
      for (let schema of schemas) {
        emptyData[schema.dataIndex] = schema?.defaultValue;
        pickedDataProps.push(schema.dataIndex);
      }
    }

    function handleSchemaUpdate(schemas) {
      setColumns(schemas);
      tableData.value = [];
      resetEmptyDataStruct(schemas);
    }

    watch(
      () => props.schemas,
      (schemas) => {
        handleSchemaUpdate(cloneDeep(schemas));
      },
      { deep: true },
    );
    watch(
      () => props.data,
      (data) => {
        tableData.value = cloneDeep(data);
      },
      { deep: true },
    );
    onMounted(() => {
      handleSchemaUpdate(props.schemas ? props.schemas : []);
    });

    const getData = async (doValidate = false) => {
      return (await getDataSource()).map((item) => pick(item, pickedDataProps))
    };

    return {
      tableData,
      registerTable,
      handleCreate,
      handleEdit,
      handleDelete,
      handleSave,
      getData,
    };
  },
});
</script>
