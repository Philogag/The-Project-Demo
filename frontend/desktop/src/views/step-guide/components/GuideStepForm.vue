<template>
  <div class="bg-white">
    <div class="m-4 ml-2">
      <BasicTitle style="width: 100%">
        <div class="form-header-left">
          <a-button
            type="primary"
            v-if="stepButtonControl.last"
            @click="handleLastStepClick"
            >上一步</a-button
          >
        </div>
        <div class="form-header-right">
          <a-button
            type="primary"
            v-if="stepButtonControl.next"
            @click="handleNextStepClick"
            >下一步</a-button
          >
          <a-button type="primary" v-else @click="handleSubmitClick">完成</a-button>
        </div>
      </BasicTitle>
      <component
        class="mt-4"
        ref="formComponentRef"
        :is="currentFormComponentName"
        :schemas="formSchema"
        :data="formData"
      />
    </div>
  </div>
</template>
<script>
import { defineComponent, nextTick, ref, reactive, onMounted, toRaw } from 'vue';
import { cloneDeep } from 'lodash-es';
import { useMessage } from '/@/hooks/web/useMessage';
import { BasicTitle } from '/@/components/Basic';
import { getUserOrganizationId } from '/@/tools/checkRole';
import { isFunction } from '/@/utils/is';
import { apiExecStepGuide } from '/@/api/step-guide';
import StepBasicForm from './form/StepBasicForm.vue';
import StepTableForm from './form/StepTableForm.vue';
import { useStepGuideStore } from '../utility/step-guide.store';

export default defineComponent({
  name: 'GuideStepForm',
  components: {
    BasicTitle,
    StepBasicForm,
    StepTableForm,
  },
  model: {
    prop: 'execRunning',
    event: 'change',
  },
  props: {
    execRunning: {
      type: Boolean,
      default: false,
    }
  },
  emits: ['success', 'register', 'next-step', 'last-step', 'update:execRunning'],
  setup(_, { emit }) {
    const { createMessage } = useMessage();
    const stepGuideStore = useStepGuideStore();
    const stepButtonControl = reactive({
      last: false,
      next: true,
    });

    const execRunning = ref(false);
    const currentFormComponentName = ref('');
    const formComponentRef = ref(null); // 表单组件对象，用于调用获取数据
    const formSchema = ref(null); // 表单结构
    const formData = ref(null); // 表单数据，仅用于步骤切换时初始化内容，不可读取

    const loadFormSchema = async () => {
      console.log('------- Change Step -------');
      const stepSchema = stepGuideStore.getCurrentStepSchema;
      if (stepSchema !== undefined) {
        stepButtonControl.last = Boolean(stepSchema.lastStepId);
        stepButtonControl.next = Boolean(stepSchema.nextStepId);

        formSchema.value = []; // 切换组件前清空schema
        formData.value = null;
        currentFormComponentName.value = stepSchema.formComponent;

        // 加载结构
        // console.log('Reload form schema.');
        formSchema.value = isFunction(stepSchema.formSchema)
          ? await stepSchema.formSchema(stepGuideStore.getStepValueMap)
          : stepSchema.formSchema;
        // 加载缓存数据
        for (let i = 0; i < 3; i++) await nextTick();
        // console.log('Reload form data.');
        formData.value = stepGuideStore.getCurrentStepFormValue ?? null;
        for (let i = 0; i < 3; i++) await nextTick();
        console.log('Reload form done.');
      }
    };
    onMounted(loadFormSchema);

    async function saveFormToCache(doValidate = true) {
      const values = await formComponentRef.value.getData(doValidate);
      console.log('Step data: ', values);
      stepGuideStore.setCurrentStepResult(values);
    }
    async function submitStepGuide() {
      await saveFormToCache(true);
      if (stepGuideStore.handleBeforeExec()) {
        emit('update:execRunning', true);
        const data = stepGuideStore.getStepValueMap;
        const obj = [...data.entries()].reduce((obj, [key, value]) => (obj[key] = toRaw(value), obj), {})
        console.log(obj);
        apiExecStepGuide({
          organizationId: getUserOrganizationId(),
          method: stepGuideStore.getMethodName,
          name: stepGuideStore.getName,
          data: obj,
        }).then(() => {
          createMessage.success('向导执行成功！');
        }).then(() => {
          // finally
          emit('update:execRunning', false);
        })
      }
    }

    return {
      stepButtonControl,
      currentFormComponentName,
      formComponentRef,
      formSchema,
      formData,
      submitStepGuide,
      loadFormSchema,
      saveFormToCache,
    };
  },
  methods: {
    reloadForm() {
      this.loadFormSchema();
    },
    async handleNextStepClick() {
      await this.saveFormToCache(true);
      await nextTick();
      this.$emit('next-step');
    },
    async handleLastStepClick() {
      await this.saveFormToCache(false);
      await nextTick();
      this.$emit('last-step');
    },
    async handleSubmitClick() {
      await this.submitStepGuide();
    },
  },
});
</script>
<style>
.form-header {
  width: max-content;
}

.form-header-block {
  float: left;
  width: fit-content;
}

.form-header-right {
  margin-left: auto;
  float: right;
}
</style>
