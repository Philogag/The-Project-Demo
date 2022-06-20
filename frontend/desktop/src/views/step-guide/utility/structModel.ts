import { FormSchema } from '/@/components/Form';
import { BasicColumn } from '/@/components/Table';

export type FromComponentType =
  | 'StepBasicForm' // Form of Vben
  | 'StepTableForm'; // multiple Form of Vben

/*
 * 创建引导项目步骤
 * */
export interface GuideStepSchema {
  stepId: string;
  stepTitle: string;
  index?: string;
  formComponent: FromComponentType;
  formSchema:
    | FormSchema[]
    | ((formValue: Map<string | number, object>) => FormSchema[])
    | BasicColumn[]
    | ((formValue: Map<string | number, object>) => BasicColumn[]);

  childStepSchemaGenerate?: (formValue: Map<string | number, object>) => GuideStepSchema[];
  lastStepId?: string;
  nextStepId?: string;
}

/*
 * 创建引导项目
 * */

export interface GuideSchema {
  methodName: string;
  stepSchema: GuideStepSchema[];

  // 获取向导内容主名称
  getName: ((formValue?: Map<string | number, object>) => string);
  // 提交执行前前端检查，return false中断
  handleBeforeExec?: ((formValue: Map<string | number, object>) => boolean | void)
}
