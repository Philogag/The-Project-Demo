import { defHttp } from '/@/utils/http/axios';
import { Result } from '/#/axios';

enum Api {
  ExecStepGuide = '/step-guide/exec',
}

export const apiExecStepGuide = (data) => {
  return defHttp.post<Result>({
    url: `${Api.ExecStepGuide}`,
    params: data
  });
};