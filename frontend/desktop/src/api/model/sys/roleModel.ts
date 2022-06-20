

export interface RoleListItem {
  role_name: string;
  code: string;
  enabled: boolean;
  editable: boolean;
}

export interface RoleList {
  data: RoleListItem[];
}
