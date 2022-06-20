import { defHttp } from '/@/utils/http/axios';
import { Result } from '/#/axios';
import { OrganizationItem, OrganizationListResult } from '/@/api/model/sys/organizationModel';
import { BasicPageQuery, BasicSelectionResult } from '/@/api/model/baseModel';

enum Api {
  GetOrganizationListForManagement = '/organization/get-organization-management-list',
  CreateOrUpdateOrganizationItem = '/organization/create-or-update',
  DeleteOrganizationItem = '/organization/delete',
  GetOrganizationSelection = '/organization/get-selection',
  GetGuestLoginOrganizationSelection = '/organization/guest-login-selection',
}


export const apiGetOrganizationList = (params: BasicPageQuery) => {
  return defHttp.post<OrganizationListResult>({
    url: Api.GetOrganizationListForManagement,
    params,
  });
};

export const apiCreateOrUpdateOrganizationItem = (params: OrganizationItem) => {
  return defHttp.post<Result>(
    {
      url: Api.CreateOrUpdateOrganizationItem,
      params,
    },
    {
      isTransformResponse: false,
    },
  );
};

export const apiDeleteOrganizationItem = (id: string) => {
  return defHttp.get<Result>(
    {
      url: `${Api.DeleteOrganizationItem}/${id}`,
    },
    {
      isTransformResponse: false,
    },
  );
};

export const apiGetOrganizationSelection = (params) => {
  return defHttp.post<BasicSelectionResult[]>({
    url: Api.GetOrganizationSelection,
    params,
  });
};

export const apiGetGuestLoginOrganizationSelection = () => {
  return defHttp.get<BasicSelectionResult[]>({
    url: Api.GetGuestLoginOrganizationSelection,
  });
};
