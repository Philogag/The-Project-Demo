import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { apiGetRoleList } from '/@/api/system-config/role';
import { apiGetOrganizationSelection } from '/@/api/system-config/ortanization';

export const columns: BasicColumn[] = [
  {
    title: '用户名',
    dataIndex: 'username',
    width: 180,
    align: 'center',
  },
  // {
  //   title: '昵称',
  //   dataIndex: 'nickName',
  //   width: 180,
  //   align: 'center',
  // },
  {
    title: '组织',
    dataIndex: 'organizationName',
    width: 240,
    align: 'center',
  },
  {
    title: '角色',
    dataIndex: 'roles',
    customRender: ({ record }) => {
      return record.roleList.map((role) => role.roleName).join(' | ');
    },
  },
  {
    title: '登录记录',
    dataIndex: 'lastLoginAt',
    width: 240,
  },
  // {
  //   title: '状态',
  //   dataIndex: 'enabled',
  //   width: 80,
  //   customRender: ({ record }) => {
  //     const enable = record.enabled;
  //     const color = enable ? 'green' : 'red';
  //     const text = enable ? '启用' : '停用';
  //     return h(Tag, { color: color }, () => text);
  //   },
  // },
];

// @ts-ignore
// @ts-ignore
export const formSchema: FormSchema[] = [
  {
    field: 'id',
    label: 'ID',
    component: 'Input',
    show: false,
  },
  {
    field: 'version',
    label: 'Version',
    component: 'Input',
    show: false,
  },
  // {
  //   field: '',
  //   label: '基本属性',
  //   component: 'Divider',
  //   colProps: { lg: 24, md: 24 },
  // },
  {
    field: 'username',
    label: '用户名',
    component: 'Input',
    required: true,
    componentProps: { placeholder: '请输入用户名' },
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'nickName',
    label: '昵称',
    component: 'Input',
    componentProps: { placeholder: '请输入昵称' },
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'newPassword',
    label: '重置密码',
    component: 'InputPassword',
    componentProps: {
      placeholder: '留空则不变',
    },
    colProps: { lg: 12, md: 24 },
  },
  {
    field: 'newPasswordConfirm',
    label: '确认密码',
    componentProps: { placeholder: '请重复密码' },
    component: 'InputPassword',
    colProps: { lg: 12, md: 24 },
  },
  // {
  //   field: 'enabled',
  //   label: '状态',
  //   component: 'RadioButtonGroup',
  //   defaultValue: true,
  //   componentProps: {
  //     options: [
  //       { label: '启用', value: true },
  //       { label: '禁用', value: false },
  //     ],
  //   },
  //   colProps: { lg: 24, md: 24 },
  // },
  {
    field: '',
    label: '权限配置',
    component: 'Divider',
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'organizationId',
    label: '所属组织',
    component: 'ApiSelect',
    required: true,
    componentProps: {
      api: apiGetOrganizationSelection,
    },
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'roleIdList',
    label: '角色',
    component: 'ApiSelect',
    required: true,
    componentProps: {
      api: apiGetRoleList,
      labelField: 'roleName',
      valueField: 'id',
      mode: 'multiple',
    },
    colProps: { lg: 24, md: 24 },
  },
];
