/**
 * @description: Login interface parameters
 */
import { RoleEnum } from "/@/enums/roleEnum";

export interface LoginParams {
  username: string;
  password: string;
}

export interface RoleInfo {
  roleName?: string;
  code: RoleEnum;
  id: string;
}

/**
 * @description: Login interface return value
 */
export interface LoginResultModel {
  userId: string | number;
  token: {
    accessToken: string,
    refreshToken?: string,
  };
  role: RoleInfo;
}

/**
 * @description: Get user information return value
 */
export interface GetUserInfoModel {
  roles: RoleInfo[];
  // 用户id
  userId: string | number;
  // 用户名
  username: string;
  // 真实名字
  realName: string;
  // 头像
  avatar: string;
  // 介绍
  desc?: string;
}
