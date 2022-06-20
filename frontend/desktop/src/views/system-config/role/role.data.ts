import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { h } from 'vue';
import { Tag } from 'ant-design-vue';

// @ts-ignore
export const columns: BasicColumn[] = [
  {
    title: '角色名称',
    dataIndex: 'roleName',
    width: 200,
    align: 'center',
  },
  {
    title: '角色代码',
    dataIndex: 'code',
    width: 200,
    align: 'center',
  },
  {
    title: '备注',
    dataIndex: 'comment',
    width: 240,
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
    show: false,
  },
  {
    field: 'roleName',
    label: '角色名称',
    component: 'Input',
    required: true,
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'code',
    label: '角色代码',
    component: 'Input',
    required: true,
    colProps: { lg: 24, md: 24 },
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
];
