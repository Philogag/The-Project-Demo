export interface BasicPageParams {
  page: number;
  pageSize: number;
}

export interface BasicFetchResult<T> {
  items: T[];
  total: number;
}

export interface BasicModel {
  id?: string;
  version?: number;
}

/* 后端真正接收的翻页查询, 自动驼峰转下划线 */
export interface BasicPageQuery {
  searchText?: string;
  orderColumns?: object;
  filterColumns?: object;
  pageSize: number;
  pageIndex: number;
}

/* 后端返回的翻页查询结果 */
export interface BasicPageResult<T> {
  filterCount?: number;
  pageIndex: number;
  pageSize: number;
  search?: string;
  totalCount: number;
  data: T[];
}


export interface BasicSelectionResult {
  label: string;
  value: string;
}

export interface BasicTreeSelectionResult extends BasicSelectionResult {
  children: BasicTreeSelectionResult[];
}
