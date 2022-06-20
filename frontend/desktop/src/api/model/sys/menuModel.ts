import type { RouteMeta } from 'vue-router';
import { Result } from "/#/axios";
export interface RouteItem {
  path: string;
  component: any;
  meta: RouteMeta;
  name?: string;
  alias?: string | string[];
  redirect?: string;
  caseSensitive?: boolean;
  children?: RouteItem[];
}

/**
 * @description: Get menu return value
 */
export type getMenuListResultModel = RouteItem[];

export interface MenuListItem {
  id: string;
  path: string;       // 参数格式路由, eg: /detail/:id
  realPath?: string;  // 实际跳转路由, eg: /detail/1234
  component: string;
  icon: string;
  title: string;
  name: string;
  order: number;
  routeCount?: number;
  enabled?: boolean;
  children?: MenuListItem[];
}

export interface MenuEditResult extends Result {
  data: any;
}

export interface RoleMenuListIdRequest {
  role_id: string;
  menu_id_list: string[];
}
