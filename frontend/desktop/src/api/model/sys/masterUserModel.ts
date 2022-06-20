import {BasicPageResult} from "/@/api/model/baseModel";
import {RoleListItem} from "/@/api/model/sys/roleModel";


export interface MasterUserListItem {
  username: string;
  isActive: boolean;
  lastLoginAt: Date;

  organizationId?: string;
  organizationName?: string;

  roleList?: RoleListItem[];
}

export interface MasterUserListResult extends BasicPageResult<MasterUserListItem> {
  data: MasterUserListItem[];
}

export interface MasterUserEditModel {
  username: string;
  isActive: boolean;

  newPassword?: string;
  newPasswordConfirm?: string;

  organizationId?: string;

  roleIdList?: string[];
}
