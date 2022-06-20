import { useUserStore } from '/@/store/modules/user';
import { RoleEnum } from '/@/enums/roleEnum';

const userStore = useUserStore();

export const getUserCurrentRole = () => {
  return userStore.getUserInfo.currentRole.code;
};

export const isSuperAdmin = () => {
  return getUserCurrentRole() === RoleEnum.SUPER;
};

export const getUserOrganizationId = () => {
  return userStore.getUserInfo.organizationId;
};
