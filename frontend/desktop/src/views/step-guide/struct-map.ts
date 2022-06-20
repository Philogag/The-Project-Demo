/*
 * 由路由参数获取表单结构
 * */

import { GuideSchema } from '/@/views/step-guide/utility/structModel';

export async function importGuideSchema(method: string): Promise<GuideSchema> {
  const schema = await import(`./struct/${method}.ts`);
  return schema.default as unknown as GuideSchema;
}
