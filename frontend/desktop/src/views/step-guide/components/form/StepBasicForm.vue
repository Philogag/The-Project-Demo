<template>
  <div v-if="!reloading">
    <BasicForm @register="registerForm" />
  </div>
</template>
<script>
  import { defineComponent, onMounted, watch, nextTick, ref, computed } from 'vue';
  import { BasicForm, useForm } from '/@/components/Form';
  import { cloneDeep } from 'lodash-es';
  import { stepBasicFormProps } from './props';

  export default defineComponent({
    name: 'StepBasicForm',
    components: {
      BasicForm,
    },
    props: stepBasicFormProps,
    setup(props) {
      const reloading = ref(false);
      const [registerForm, { getFieldsValue, setFieldsValue, validate, resetSchema, resetFields }] =
        useForm({
          labelWidth: 140,
          schemas: props.schemas,
          showActionButtonGroup: false,
          baseColProps: { lg: 12, md: 24 },
        });
      
      const getDefaultValue = () => {
        const res = {};
        for (let schema of props.schemas){
          if (schema.field && schema.defaultValue !== undefined)
            res[schema.field] = schema.defaultValue;
        }
        return res;
      }

      watch(
        () => props.schemas,
        async (schemas) => {
          await resetSchema([]);
          await nextTick();
          await resetSchema(schemas);
          // console.log('Set form schema: ', schemas);
          await nextTick();
        },
        { deep: true },
      );

      watch(
        () => props.data,
        async (data) => {
          await resetFields();
          await nextTick();
          await setFieldsValue(getDefaultValue());
          if (data) await setFieldsValue(data);
          // console.log('Set form data: ', data);
        },
        { deep: true },
      );
      onMounted(async () => {
        await setFieldsValue(getDefaultValue());
        if (props.data) await setFieldsValue(props.data);
      });

      const getData = async (doValidate = false) => {
        if (doValidate) await validate();
        return cloneDeep(await getFieldsValue());
      };

      return {
        reloading,
        registerForm,
        getData,
      };
    },
  });
</script>
