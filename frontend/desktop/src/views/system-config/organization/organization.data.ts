import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { h } from 'vue';
import { Tag } from 'ant-design-vue';

export const columns: BasicColumn[] = [
  {
    title: '组织名称',
    dataIndex: 'name',
    width: 180,
    align: 'left',
  },
  {
    title: '组织代码',
    dataIndex: 'code',
    align: 'center',
    width: 180,
    ellipsis: false,
  },
  {
    title: '地区',
    dataIndex: 'areaFullName',
    width: 220,
    align: 'center',
  },
  {
    title: '备注',
    dataIndex: 'comment',
    width: 220,
    align: 'center',
  },
  {
    title: '状态',
    dataIndex: 'enabled',
    width: 80,
    customRender: ({ record }) => {
      const enable = record.enabled;
      const color = enable ? 'green' : 'red';
      const text = enable ? '启用' : '停用';
      return h(Tag, { color: color }, () => text);
    },
  },
  {
    title: '访客登录',
    dataIndex: 'guestEnabled',
    width: 80,
    customRender: ({ record }) => {
      const enable = record.guestEnabled;
      const color = enable ? 'green' : 'red';
      const text = enable ? '启用' : '停用';
      return h(Tag, { color: color }, () => text);
    },
  },
];

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
    defaultValue: 1,
    show: false,
  },
  {
    field: 'name',
    label: '组织名称',
    component: 'Input',
    required: true,
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'code',
    label: '菜单代码',
    component: 'Input',
    required: true,
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'areaId',
    label: '地区',
    component: 'Input',
    // component: 'ApiTreeSelect',
    // componentProps: {
    //   api: () => {}
    // },
    // required: true,
    // colProps: { lg: 24, md: 24 },
  },
  {
    field: 'comment',
    label: '备注',
    component: 'InputTextArea',
    componentProps: { rows: 3 },
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'enabled',
    label: '状态',
    component: 'RadioButtonGroup',
    defaultValue: true,
    componentProps: {
      options: [
        { label: '启用', value: true },
        { label: '禁用', value: false },
      ],
    },
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'guestEnabled',
    label: '状态',
    component: 'RadioButtonGroup',
    defaultValue: true,
    componentProps: {
      options: [
        { label: '启用', value: true },
        { label: '禁用', value: false },
      ],
    },
    colProps: { lg: 24, md: 24 },
  },
];
