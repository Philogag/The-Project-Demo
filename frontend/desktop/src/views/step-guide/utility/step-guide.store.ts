import { defineStore } from 'pinia';
import { GuideStepSchema } from '/@/views/step-guide/utility/structModel';

interface StepGuideState {
  methodName?: string;
  currentStepId?: string;
  stepSchema: Map<string | number, GuideStepSchema>;
  stepFormValue: Map<string | number, object>;
  fnGetName?: ((formValue?: Map<string | number, object>) => string);
  fnHandleBeforeExec?: ((formValue?: Map<string | number, object>) => boolean | void)
}

export const useStepGuideStore = defineStore({
  id: 'step-guide',
  state: (): StepGuideState => ({
    // method name of guide
    methodName: undefined,
    //
    currentStepId: undefined,
    // Step schema order by step_id
    stepSchema: new Map<string | number, GuideStepSchema>(),
    // Step value order by step_id
    stepFormValue: new Map<string | number, object>(),
    // 
    fnGetName: () => '',
    fnHandleBeforeExec: undefined,
  }),
  getters: {
    getMethodName(): string {
      return this.methodName ?? '';
    },
    getCurrentStepId(): string {
      return this.currentStepId ?? '';
    },
    getCurrentStepSchema(): GuideStepSchema | undefined {
      if (this.currentStepId) return this.stepSchema.get(this.currentStepId);
    },
    getStepValueMap(): Map<string | number, object> {
      return this.stepFormValue;
    },
    getCurrentStepFormValue(): object | undefined {
      if (this.currentStepId) return this.stepFormValue.get(this.currentStepId);
    },
    
    getName(): string {
      return this.fnGetName 
        ? this.fnGetName(this.stepFormValue)
        : '';
    },
  },
  actions: {
    resetState() {
      this.methodName = undefined;
      this.currentStepId = undefined;
      this.stepSchema = new Map<string | number, GuideStepSchema>();
      this.stepFormValue = new Map<string | number, object>();
      this.fnGetName = () => '';
      this.fnHandleBeforeExec = undefined;
    },
    setMethodName(methodName: string) {
      this.methodName = methodName;
    },
    setCurrentStepId(stepId: string) {
      this.currentStepId = stepId;
    },
    setStepSchema(schema: GuideStepSchema) {
      this.stepSchema.set(schema.stepId, schema);
    },
    setCurrentStepResult(values: object) {
      if (this.currentStepId) this.stepFormValue.set(this.currentStepId, values);
    },
    setFnGetName(fn: ((formValue?: Map<string | number, object>) => string)) {
      this.fnGetName = fn;
    },
    setFnHandleBeforeExec(fn: ((formValue?: Map<string | number, object>) => boolean | void)) {
      this.fnHandleBeforeExec = fn;
    },
    handleBeforeExec(): boolean {
      return this.fnHandleBeforeExec
        ? !(this.fnHandleBeforeExec(this.stepFormValue) === false)
        : true;
    }
  },
});
