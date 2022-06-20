import { defHttp } from '/@/utils/http/axios';
import { BasicSelectionResult } from '/@/api/model/baseModel';

export enum EnumResultType {
  dict = 'dict',
  map = 'tuple',
  selection = 'selection',
}

/**
 * @description: Get user menu based on id
 */
export const apiGetEnumDict = (enum_name) => {
  return defHttp.get<any>({ url: `/enum/dict/${enum_name}` });
};

/*
 * enum_name:
 *
 *    role_code => EnumRoleCode
 * */
export const apiGetEnumMap = (enum_name) => {
  return new Promise<Map<string, string>>((resolve) => {
    defHttp.get<any>({ url: `/enum/tuple/${enum_name}` }).then((result) => {
      resolve(new Map(result));
    });
  });
};

/*
 * enum_name:
 *
 *    role_code => EnumRoleCode
 * */
export const apiGetEnumSelection = (enum_name) => {
  return defHttp.get<BasicSelectionResult[]>({ url: `/enum/selection/${enum_name}` });
};
