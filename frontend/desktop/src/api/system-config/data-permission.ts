import { defHttp } from '/@/utils/http/axios';
import { Result } from '/#/axios';

const Api = {
  GetPermittedUserPage: '/data-permission/get-permitted-user-page',
  AddDataPermissionItem: '/data-permission/set-data-permission-item',
  DeleteDataPermissionItem: '/data-permission/delete-data-permission-item',
};

export const apiAddDataPermission = (params) => {
  return defHttp.post<Result>({
    url: Api.AddDataPermissionItem,
    params,
  });
};

export const apiDeleteDataPermission = (params) => {
  return defHttp.post<Result>({
    url: Api.DeleteDataPermissionItem,
    params,
  });
};

export const apiGetPermittedUserPage = (
  permitted_object_category: string,
  permitted_object_id: string,
  pageParams,
  invert = false,
) => {
  return defHttp.post<Result>({
    url: `${Api.GetPermittedUserPage}/${permitted_object_category}/${permitted_object_id}?invert=${invert}`,
    params: pageParams,
  });
};
