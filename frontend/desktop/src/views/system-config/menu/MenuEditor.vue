<template>
  <BasicDrawer
    v-bind="$attrs"
    @register="registerDrawer"
    showFooter
    :title="getTitle"
    width="45%"
    @ok="handleSubmit"
  >
    <BasicForm @register="registerForm" />
  </BasicDrawer>
</template>
<script lang="ts">
  import { defineComponent, ref, computed, unref } from 'vue';
  import { BasicForm, useForm } from '/@/components/Form/index';
  import { formSchema } from './menu.data';
  import { BasicDrawer, useDrawerInner } from '/@/components/Drawer';
  import { apiCreateOrUpdateMenuItem, getMenuListForManager } from '/@/api/system-config/menu';
  import { MenuListItem } from '/@/api/model/sys/menuModel';
  import { useMessage } from '/@/hooks/web/useMessage';
  export default defineComponent({
    name: 'MenuEditor',
    components: { BasicDrawer, BasicForm },
    emits: ['success', 'register'],
    setup(_, { emit }) {
      const { notification } = useMessage();
      const isUpdate = ref(true);
      const [registerForm, { resetFields, setFieldsValue, validate, updateSchema }] = useForm({
        labelWidth: 100,
        schemas: formSchema,
        showActionButtonGroup: false,
        baseColProps: { lg: 12, md: 24 },
      });

      const build_simple_selection = (treeData: MenuListItem[]) => {
        return treeData.map((item) => ({
          value: item.id,
          label: item.title,
          children: item.children ? build_simple_selection(item.children) : [],
        }));
      };
      const get_parent_id_selection = async () => {
        let treeData = await getMenuListForManager();
        treeData = build_simple_selection(treeData);
        console.log(treeData);
        return treeData;
      };

      const [registerDrawer, { setDrawerProps, closeDrawer }] = useDrawerInner(async (data) => {
        resetFields();
        setDrawerProps({ confirmLoading: false });
        isUpdate.value = !!data?.isUpdate;

        if (unref(isUpdate)) {
          data.record.type = data.record?.component === 'LAYOUT' ? '0' : '1';
          setFieldsValue({
            ...data.record,
          });
        }

        let treeData = await get_parent_id_selection();
        updateSchema({
          field: 'parentId',
          componentProps: { treeData },
        });
      });
      const getTitle = computed(() => (!unref(isUpdate) ? '新增菜单' : '编辑菜单'));
      async function handleSubmit() {
        try {
          const values = await validate();
          setDrawerProps({ confirmLoading: true });
          // console.log(values);
          if (values.type === '0') values.component = 'LAYOUT';
          apiCreateOrUpdateMenuItem(values).then((res) => {
            if (res.message.length == 0) {
              closeDrawer();
              emit('success');
            } else {
              notification.error({
                message: '错误',
                description: res.message.join('\n'),
              });
            }
          });
        } finally {
          setDrawerProps({ confirmLoading: false });
        }
      }
      return { registerDrawer, registerForm, getTitle, handleSubmit };
    },
  });
</script>
