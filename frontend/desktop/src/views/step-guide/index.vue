<template>
  <Spin
    tip="向导执行中..." 
    :spinning="execRunning"
    size="large"
  >
    <template #indicator>
      <LoadingOutlined />
    </template>
    <PageWrapper contentClass="flex w-full" class="fill-height w-full">
      <GuideStepTree class="w-1/5 mr-4" ref="stepTreeRef" @reload-form="handleReloadForm" />
      <GuideStepForm
        class="w-4/5"
        ref="stepFormRef"
        @next-step="handleNextStep"
        @last-step="handleLastStep"
        v-model:execRunning="execRunning"
      />
    </PageWrapper>
  </Spin>
</template>
<script>
  import { defineComponent, ref, nextTick } from 'vue';
  import { Spin } from 'ant-design-vue';
  import { LoadingOutlined } from '@ant-design/icons-vue'
  import { PageWrapper } from '/@/components/Page';
  import GuideStepTree from './components/GuideStepTree.vue';
  import GuideStepForm from './components/GuideStepForm.vue';

  export default defineComponent({
    name: 'StepGuide',
    components: {
      PageWrapper,
      Spin,
      GuideStepTree,
      GuideStepForm,
      LoadingOutlined,
    },
    setup() {
      const stepTreeRef = ref(null);
      const stepFormRef = ref(null);
      const execRunning = ref(false);
      return {
        stepTreeRef,
        stepFormRef,
        execRunning
      };
    },
    methods: {
      // Tree与Form的事件通信中继，调用前需nextTick
      // 不得使用箭头函数，会导致this失效
      handleReloadForm() {
        // 接收到树切换节点，重新加载表单
        this.$refs.stepFormRef.reloadForm();
      },
      handleNextStep() {
        // 接收到表单按钮，进入下一步
        console.log('go next');
        this.$refs.stepTreeRef.nextStep();
      },
      handleLastStep() {
        // 接收到表单按钮，退回上一步
        console.log('return last');
        this.$refs.stepTreeRef.lastStep();
      },
    },
  });
</script>
<style scoped>
  .fill-height {
    min-height: 100%;
    display: flex;
  }
</style>
