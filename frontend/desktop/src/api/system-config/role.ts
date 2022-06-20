import { defHttp } from '/@/utils/http/axios';
import { RoleList, RoleListItem } from '../model/sys/roleModel';
import { Result } from '/#/axios';

enum Api {
  SwitchCurrentRole = '/role/switch-current-role',
  GetRoleListForManagement = '/role/get-role-management-list',
  CreateOrUpdateRoleItem = '/role/create-or-update',
  DeleteRoleItem = '/role/delete',
}

export const apiSwitchCurrentRole = (role_id: string) => {
  return defHttp.get<Result>({ url: `${Api.SwitchCurrentRole}/${role_id}` });
};

export const apiGetRoleList = () => {
  return defHttp.get<RoleList>({ url: Api.GetRoleListForManagement });
};

export const apiCreateOrUpdateRoleItem = (params: RoleListItem) => {
  return defHttp.post<Result>(
    {
      url: Api.CreateOrUpdateRoleItem,
      params,
    },
    {
      isTransformResponse: false,
    },
  );
};

export const apiDeleteRoleItem = (role_id: string) => {
  return defHttp.get<Result>(
    { url: `${Api.DeleteRoleItem}/${role_id}` },
    {
      isTransformResponse: false,
    },
  );
};
