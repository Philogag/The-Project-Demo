import { OrganizationItem } from './../model/sys/organizationModel';
import { defHttp } from '/@/utils/http/axios';
import { LoginParams, LoginResultModel} from '../model/sys/userModel';

import { ErrorMessageMode } from '/#/axios';
import { UserInfo } from "/#/store";

enum Api {
  Login = '/auth/login',
  Logout = '/auth/logout',
  GetUserInfo = '/master-user/get-current-user-info',
  GetPermCode = '/getPermCode',
  GuestLogin = '/auth/login/guest',
}

/**
 * @description: user login api
 */
export function loginApi(params: LoginParams, mode: ErrorMessageMode = 'modal') {
  return defHttp.post<LoginResultModel>(
    {
      url: Api.Login,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
}

/**
 * @description: guest user login api
 */
export function guestLoginApi(params, mode: ErrorMessageMode = 'modal') {
  return defHttp.get<LoginResultModel>(
    {
      url: `${Api.GuestLogin}/${params.organizationId}`,
    },
    {
      errorMessageMode: mode,
    },
  );
}

/**
 * @description: getUserInfo
 */
export function getUserInfo() {
  return defHttp.get<UserInfo>({ url: Api.GetUserInfo }, { errorMessageMode: 'none' });
}

export function getPermCode() {
  return defHttp.get<string[]>({ url: Api.GetPermCode });
}

export function doLogout() {
  return defHttp.get({ url: Api.Logout });
}
