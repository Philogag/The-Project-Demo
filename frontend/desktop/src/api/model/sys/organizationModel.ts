import {BasicPageResult} from "/@/api/model/baseModel";


export interface OrganizationItem {
  name: string;
  code: string;
  areaId: string;
  comment?: string;
  enabled: boolean;
}

export interface OrganizationListItem extends OrganizationItem {
  areaPath?: string[];
  areaFullName?: string;
}

export interface OrganizationListResult extends BasicPageResult<OrganizationListItem> {
  data: OrganizationListItem[];
}
