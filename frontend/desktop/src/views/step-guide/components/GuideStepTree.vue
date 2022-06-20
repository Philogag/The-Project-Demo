<template>
  <BasicTree
    ref="stepTreeRef"
    :treeData="treeData"
    v-model:selectedKeys="currentStepId"
    title="步骤"
    @select="reloadForm"
  >
    <template #title="item">
      {{ item.index }}. {{ item.name }}
      <div class="ml-1">
        <Icon v-if="item.status === 'empty'" icon="ant-design:info-circle" color="grey" />
        <Icon v-else-if="item.status === 'done'" icon="ant-design:check-circle" color="green" />
        <Icon v-else icon="ant-design:warning" color="orange" />
      </div>
    </template>
  </BasicTree>
</template>

<script>
  import { defineComponent, ref, nextTick, onMounted, unref } from 'vue';
  import { BasicTree } from '/@/components/Tree';

  import { useStepGuideStore } from '../utility/step-guide.store';
  import { importGuideSchema } from '../struct-map';
  import { useRoute } from 'vue-router';
  import { Icon } from '/@/components/Icon';

  export default defineComponent({
    name: 'GuideStepTree',
    components: { BasicTree, Icon },
    emits: ['success', 'register', 'reload-form'],
    setup(_, { emit }) {
      const route = useRoute();
      const method = route.path.split('/')[2];
      const stepGuideStore = useStepGuideStore();

      const stepTreeRef = ref(null);
      const currentStepId = ref([]);
      const treeData = ref([]);
      const reloadForm = () => {
        const stepId = currentStepId.value[0];
        stepGuideStore.setCurrentStepId(stepId);
        emit('reload-form'); // 通知表单组件重载
      };

      function getTree() {
        const tree = unref(stepTreeRef);
        if (!tree) {
          throw new Error('tree is null!');
        }
        return tree;
      }

      onMounted(async () => {
        importGuideSchema(method).then((guideSchema) => {
          stepGuideStore.resetState();
          stepGuideStore.setMethodName(guideSchema.methodName);
          stepGuideStore.setFnGetName(guideSchema.getName);
          stepGuideStore.setFnHandleBeforeExec(guideSchema.handleBeforeExec);
          treeData.value = [];
          let index = 0;
          guideSchema.stepSchema.forEach((stepSchema) => {
            treeData.value.push({
              key: stepSchema.stepId,
              name: stepSchema.stepTitle,
              index: (index += 1),
              nextStepId: stepSchema.nextStepId,
              status: 'empty',
              selectable: index === 1,
              slots: { title: 'title' },
            });
            stepGuideStore.setStepSchema(stepSchema);
          });
          currentStepId.value = [treeData.value[0].key];
          nextTick(nextTick(reloadForm));
        });
      });

      const generateChildStep = () => {
        const stepSchema = stepGuideStore.getCurrentStepSchema;
        // console.log(stepSchema);
        if (stepSchema.childStepSchemaGenerate !== undefined) {
          // goto child step, if not in tree generate
          // TODO[desktop] goto child step
          //
        } else {
        }
        return stepSchema.nextStepId;
      };

      const setCurrentStep = (stepId) => {
        console.log("Current Step: ", stepId);
        currentStepId.value = [stepId];
        stepGuideStore.setCurrentStepId(stepId);
        getTree().updateNodeByKey(stepId, { selectable: true });
      };

      return {
        stepTreeRef,
        treeData,
        currentStepId,
        stepGuideStore,
        reloadForm,
        generateChildStep,
        setCurrentStep,
        getTree,
      };
    },
    methods: {
      nextStep() {
        // 前进到下一步
        this.getTree().updateNodeByKey(this.currentStepId[0], { status: 'done' });
        const stepId = this.generateChildStep();
        this.setCurrentStep(stepId);
        nextTick(this.reloadForm);
      },
      lastStep() {
        // 退回到上一步
        this.getTree().updateNodeByKey(this.currentStepId[0], { status: 'incomplete' });
        const stepId = this.stepGuideStore.getCurrentStepSchema?.lastStepId;
        this.setCurrentStep(stepId);
        nextTick(this.reloadForm);
      },
    },
  });
</script>
<style>
  .ant-tree-node-content-wrapper {
    width: fit-content !important;
  }
</style>
