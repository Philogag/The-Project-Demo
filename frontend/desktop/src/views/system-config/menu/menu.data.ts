import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { h } from 'vue';
import { Tag } from 'ant-design-vue';
import { Icon } from '/@/components/Icon';

export const columns: BasicColumn[] = [
  {
    title: '菜单名称',
    dataIndex: 'title',
    width: 180,
    align: 'left',
  },
  {
    title: '排序',
    dataIndex: 'order',
    align: 'center',
    width: 120,
    ellipsis: false,
  },
  {
    title: '菜单代码',
    dataIndex: 'name',
    width: 210,
    align: 'center',
  },
  {
    title: '图标',
    dataIndex: 'icon',
    width: 60,
    customRender: ({ record }) => {
      return h(Icon, { icon: record.icon });
    },
  },
  {
    title: '组件',
    dataIndex: 'component',
    customRender: ({ record }) => {
      return record.component === 'LAYOUT' ? '文件夹' : record.component;
    },
  },
  {
    title: '数据权限',
    dataIndex: 'routeCount',
    width: 80,
    customRender: ({ record }) => {
      return record.component === 'LAYOUT' || record.routeCount == undefined || record.routeCount === 0 ? '-' : record.routeCount;
    },
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
];

const isDir = (type: string) => type === '0';
const isMenu = (type: string) => type === '1';


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
  {
    field: 'type',
    label: '菜单类型',
    component: 'RadioButtonGroup',
    defaultValue: '0',
    componentProps: {
      options: [
        { label: '文件夹', value: '0' },
        { label: '菜单', value: '1' },
      ],
    },
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'title',
    label: '菜单名称',
    component: 'Input',
    required: true,
  },
  {
    field: 'name',
    label: '菜单代码',
    component: 'Input',
    required: true,
  },
  {
    field: 'parentId',
    label: '上级菜单',
    component: 'TreeSelect',
    componentProps: {},
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'order',
    label: '排序',
    component: 'InputNumber',
    required: true,
  },
  {
    field: 'icon',
    label: '图标',
    component: 'Input',
    defaultValue: '',
    required: true,
  },
  {
    field: 'path',
    label: '路由地址',
    component: 'Input',
    required: true,
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'redirect',
    label: '重定向',
    component: 'Input',
    required: false,
    ifShow: ({ values }) => isDir(values.type),
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'component',
    label: '组件路径',
    component: 'Input',
    required: ({ values }) => isMenu(values.type),
    ifShow: ({ values }) => isMenu(values.type),
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
  // {
  //   field: 'isExt',
  //   label: '是否外链',
  //   component: 'RadioButtonGroup',
  //   defaultValue: '0',
  //   componentProps: {
  //     options: [
  //       { label: '否', value: '0' },
  //       { label: '是', value: '1' },
  //     ],
  //   },
  // },
];
