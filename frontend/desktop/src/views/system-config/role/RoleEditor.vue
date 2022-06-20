<template>
  <BasicDrawer
    v-bind="$attrs"
    @register="registerDrawer"
    showFooter
    :title="getTitle"
    width="30%"
    @ok="handleSubmit"
  >
    <BasicForm @register="registerForm" />
  </BasicDrawer>
</template>
<script lang="ts">
  import { defineComponent, ref, computed, unref } from 'vue';
  import { BasicForm, useForm } from '/@/components/Form/index';
  import { formSchema } from './role.data';
  import { BasicDrawer, useDrawerInner } from '/@/components/Drawer';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { apiCreateOrUpdateRoleItem } from '/@/api/system-config/role';
  export default defineComponent({
    name: 'RoleEditor',
    components: { BasicDrawer, BasicForm },
    emits: ['success', 'register'],
    setup(_, { emit }) {
      const { notification } = useMessage();
      const isUpdate = ref(true);
      const [registerForm, { resetFields, setFieldsValue, validate }] = useForm({
        labelWidth: 100,
        schemas: formSchema,
        showActionButtonGroup: false,
        baseColProps: { lg: 12, md: 24 },
      });
      const [registerDrawer, { setDrawerProps, closeDrawer }] = useDrawerInner(async (data) => {
        resetFields();
        setDrawerProps({ confirmLoading: false });
        isUpdate.value = !!data?.isUpdate;

        if (unref(isUpdate)) {
          setFieldsValue({
            ...data.record,
          });
        }
      });
      const getTitle = computed(() => (!unref(isUpdate) ? '新建角色' : '编辑角色'));
      async function handleSubmit() {
        try {
          const values = await validate();
          setDrawerProps({ confirmLoading: true });
          apiCreateOrUpdateRoleItem(values).then((res) => {
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
