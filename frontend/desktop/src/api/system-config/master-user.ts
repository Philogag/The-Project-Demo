import { defHttp } from '/@/utils/http/axios';
import { BasicPageQuery } from '/@/api/model/baseModel';
import { MasterUserEditModel, MasterUserListResult } from '/@/api/model/sys/masterUserModel';
import { Result } from '/#/axios';

enum Api {
  GetMasterUserListForManagement = '/master-user/get-master-user-management-list',
  CreateOrUpdateMasterUser = '/master-user/create-or-update',
  DeleteMasterUserById = '/master-user/delete',
}

/**
 * @description: user login api
 */
export const apiGetMasterUserList = (params: BasicPageQuery) => {
  return defHttp.post<MasterUserListResult>({ url: Api.GetMasterUserListForManagement, params });
};

export const apiCreateOrUpdateMasterUser = (params: MasterUserEditModel) => {
  return defHttp.post<Result>(
    {
      url: Api.CreateOrUpdateMasterUser,
      params,
    },
    {
      isTransformResponse: false,
    },
  );
};

export const apiDeleteMasterUserById = (id: string) => {
  return defHttp.get<Result>(
    { url: `${Api.DeleteMasterUserById}/${id}` },
    {
      isTransformResponse: false,
    },
  );
};
