import { defHttp } from '/@/utils/http/axios';
import {
  MenuEditResult,
  MenuListItem,
  RoleMenuListIdRequest,
  RouteItem,
} from '../model/sys/menuModel';
import { Result } from '/#/axios';

enum Api {
  GetMenuListForManager = '/menu/get-menu-management-list',
  CreateOrUpdateMenuItem = '/menu/create-or-update',
  DeleteMenuItem = '/menu/delete',
  GetRoleMenuIdList = '/menu/get-role-menu-id-list',
  SetRoleMenuIdList = '/menu/set-role-menu-id-list',
  GetMenuDataRouteIdList = '/menu/get-menu-data-route-list',
  SetMenuDataRouteIdList = '/menu/set-menu-data-route-list',
  ClearMenuDataRouteIdList = '/menu/clear-menu-data-route-list',
}

/**
 * @description: 获取所有菜单项以供系统配置
 */
export const getMenuListForManager = () => {
  return defHttp.get<MenuListItem[]>({
    url: Api.GetMenuListForManager,
  });
};

export const apiCreateOrUpdateMenuItem = (params: RouteItem) => {
  return defHttp.post<MenuEditResult>(
    {
      url: Api.CreateOrUpdateMenuItem,
      params,
    },
    {
      isTransformResponse: false,
    },
  );
};

export const apiDeleteMenuItem = (menuId: string) => {
  return defHttp.get<MenuEditResult>(
    {
      url: `${Api.DeleteMenuItem}/${menuId}`,
    },
    {
      isTransformResponse: false,
    },
  );
};

export const apiGetRoleMenuIdList = (roleId: string) => {
  return defHttp.get<string[]>({
    url: `${Api.GetRoleMenuIdList}/${roleId}`,
  });
};

export const apiSetRoleMenuIdList = (params: RoleMenuListIdRequest) => {
  return defHttp.post<Result>(
    {
      url: Api.SetRoleMenuIdList,
      params,
    },
    {
      isTransformResponse: false,
    },
  );
};

/* 获取菜单所需要的数据路由权限 */
export const apiGetMenuDataRouteIdList = (menuId: string) => {
  return defHttp.get<string[]>({
    url: `${Api.GetMenuDataRouteIdList}/${menuId}`,
  });
};

/* 保存菜单所需要的数据路由权限 */
export const apiSetMenuDataRouteIdList = (params) => {
  return defHttp.post<Result>({
    url: Api.SetMenuDataRouteIdList,
    params,
  });
};

export const apiClearMenuDataRouteIdList = (menuId: string) => {
  return defHttp.get<Result>({
    url: `${Api.ClearMenuDataRouteIdList}/${menuId}`,
  });
};
