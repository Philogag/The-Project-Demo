import { defHttp } from '/@/utils/http/axios';
import {
  getMenuListResultModel,
} from '../model/sys/menuModel';

enum Api {
  GetMenuList = '/menu/get-menu-list',
}

/**
 * @description: Get user menu based on id
 */

export const getMenuList = () => {
  return defHttp.get<getMenuListResultModel>({ url: Api.GetMenuList });
};
