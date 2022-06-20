import { GuideSchema } from '../utility/structModel';
import { apiGetOrganizationSelection } from '/@/api/system-config/ortanization';
import { getUserOrganizationId, isSuperAdmin } from '/@/tools/checkRole';
import { apiGetRatingCalculatorList } from '/@/api/data-view/rating-calculator';
import { apiGetTeamGroupSelectionByOrganization } from '/@/api/data-view/team-group';
import { apiGetSportLibSelection } from '/@/api/data-view/sport-lib';
import { apiGetEnumSelection } from '/@/api/sys/enum';

export const guideSchema: GuideSchema = {
  methodName: 'create_school_sport_meeting',
  getName: (guideResult) => guideResult.get('basicInfo')?.name,
  handleBeforeExec: (guideResult) => {
    let pass = true;
    let message: string[] = [];

    // if (guideResult.get('teamGenerate').length != guideResult.get('teamGroup').length) {
    //   pass = false;
    //   message.push(`未给所有参赛组配置代表队生成`);
    // }

    guideResult.get('teamGenerate').forEach((item) => {
      if (item.editable) {
        pass = false;
        message.push(`代表队生成编辑中`);
      }
    })
    guideResult.get('competitionGenerate').forEach((item) => {
      if (item.editable) {
        pass = false;
        message.push(`项目生成编辑中`);
      }
    })
    if (message.length > 0) {
      console.log(message);
      // TODO notification
    }
    return pass;
  },
  stepSchema: [
    {
      stepId: 'basicInfo',
      stepTitle: '基本信息',
      formComponent: 'StepBasicForm',
      formSchema: [
        {
          field: 'masterOrganizationId',
          label: '主办组织',
          component: 'ApiSelect',
          componentProps: {
            api: apiGetOrganizationSelection,
          },
          defaultValue: getUserOrganizationId(),
          show: isSuperAdmin(),
          required: true,
          colProps: { lg: 24, md: 24 },
        },
        {
          field: 'name',
          label: '运动会名称',
          component: 'Input',
          required: true,
          colProps: { lg: 24, md: 24 },
        },
        {
          field: 'startAt',
          label: '举办时间',
          component: 'DatePicker',
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
      ],
      nextStepId: 'generalSettings',
    },
    {
      stepId: 'generalSettings',
      stepTitle: '通用配置',
      lastStepId: 'basicInfo',
      formComponent: 'StepBasicForm',
      formSchema: (guideResult) => [
        {
          field: 'line-积分算法',
          label: '积分算法',
          component: 'Divider',
        },
        {
          field: 'ratingCalculatorId',
          label: '积分算法',
          component: 'ApiSelect',
          componentProps: {
            api: ({ id }) => {
              return id ? apiGetRatingCalculatorList(id) : [];
            },
            params: {
              // @ts-ignore
              id: guideResult.get('basicInfo')?.masterOrganizationId,
            },
            labelField: 'name',
            valueField: 'id',
          },
          required: true,
          colProps: { lg: 24, md: 24 },
        },
        {
          field: 'line-场地信息',
          label: '场地信息',
          component: 'Divider',
        },
        {
          field: 'trackNumber',
          label: '跑道数量',
          component: 'InputNumber',
          required: true,
          defaultValue: 8,
          colProps: { lg: 24, md: 24 },
        },
        {
          field: 'line-号码布模板',
          label: '号码布生成',
          component: 'Divider',
        },
        {
          field: 'numberClothTemplate',
          label: '号码布模板',
          component: 'Input',
          required: true,
          defaultValue: '{index:0:3}',
          colProps: { lg: 24, md: 24 },
          helpMessage: [
            '号码布模板，可用占位符：',
            ' - {index:0>3d}：定长序号',
            '          ||└ 填充长度',
            '          |└─ 数字对齐方向，`>`为右对齐、`<`为左对齐',
            '          └── 填充内容',
            ' --- 长度超过前补长度时，短序号不会增长，如共100队，使用{index:0>2d}时',
            ' --- 1->01, 10->10, 100-> 100',
            '样例：',
            ' - "{index:0>3d}号" -> "001号" - "123号"',
            ' - "{index:0>4d}" -> "0001" - "1234"',
          ],
        },
        {
          field: 'numberClothBegin',
          label: '号码布起始',
          component: 'InputNumber',
          defaultValue: 1,
          colProps: { lg: 24, md: 24 },
        },
      ],
      nextStepId: 'teamGroup',
    },
    {
      stepId: 'teamGroup',
      stepTitle: '配置参赛组',
      lastStepId: 'generalSettings',
      formComponent: 'StepBasicForm',
      formSchema: (guideResult) => [
        {
          field: 'allowedGroup',
          label: '参赛组',
          component: 'ApiSelect',
          componentProps: {
            api: ({ id }) => {
              return id ? apiGetTeamGroupSelectionByOrganization(id) : [];
            },
            params: {
              // @ts-ignore
              id: guideResult.get('basicInfo')?.masterOrganizationId,
            },
            mode: 'multiple',
            labelInValue: true,
          },
          required: true,
          colProps: { lg: 24, md: 24 },
        },
      ],
      nextStepId: 'teamGenerate',
    },
    {
      stepId: 'teamGenerate',
      stepTitle: '配置代表队',
      lastStepId: 'teamGroup',
      formComponent: 'StepTableForm',
      formSchema: (guideResult) => [
        {
          title: 'ID',
          dataIndex: 'id',
          editRow: false,
          ifShow: false,
        },
        {
          title: '参赛组',
          dataIndex: 'teamGroup',
          editRow: true,
          editComponent: 'ApiSelect',
          editComponentProps: {
            api: ({ id }) => {
              // @ts-ignore
              return guideResult.get('teamGroup')?.allowedGroup;
            },
            labelInValue: true,
            showSearch: true,
          },
          editRule: true, // means required.
        },
        {
          dataIndex: 'teamCount',
          title: '队伍个数',
          editComponent: 'InputNumber',
          editComponentProps: {
            min: 1,
          },
          defaultValue: 10,
          editRow: true,
        },
        {
          dataIndex: 'teamNameGenerate',
          title: '队名生成模板',
          helpMessage: [
            '代表队队名生成模板，可用占位符：',
            ' - {index:0>3d}：定长序号',
            '          ||└ 填充长度',
            '          |└─ 数字对齐方向，`>`为右对齐、`<`为左对齐',
            '          └── 填充内容',
            ' --- 长度超过前补长度时，短序号不会增长，如共100队，使用{index:0:2}时',
            '        1->01, 10->10, 100-> 100',
            '样例：',
            ' - "一（{index}）班" -> "一（1）班" - "一（10）班"',
          ],
          editRow: true,
          editRule: true,
          editComponent: 'Input',
          defaultValue: '{index:0>2d}',
        },
        {
          dataIndex: 'teamUsernameGenerate',
          title: '账号生成',
          helpMessage: [
            '账号生成模板，可用占位符：',
            ' - {index:0>3d}：定长序号',
            '          ||└ 填充长度',
            '          |└─ 数字对齐方向，`>`为右对齐、`<`为左对齐',
            '          └── 填充内容',
            ' --- 长度超过前补长度时，短序号不会增长，如共100队，使用{index:0:2}时',
            '        1->01, 10->10, 100-> 100',
            '样例：',
            ' - "2022_p1_c{index:0>2d}" -> "2022_p1_c01" ~ "2022_p1_c10"',
          ],
          editRow: true,
          editRule: true,
          editComponent: 'Input',
          defaultValue: '{index:0>2d}',
        },
        {
          dataIndex: 'peopleMaleLimit',
          title: '队员限制-男',
          helpMessage: '填0则不限',
          editComponent: 'InputNumber',
          defaultValue: 5,
          editRow: true,
          editRule: true,
        },
        {
          dataIndex: 'peopleFemaleLimit',
          title: '队员限制-女',
          helpMessage: '填0则不限',
          editComponent: 'InputNumber',
          defaultValue: 5,
          editRow: true,
          editRule: true,
        },
        {
          dataIndex: 'competitionPerPeople',
          title: '每人限报',
          helpMessage: '填0则不限',
          editComponent: 'InputNumber',
          defaultValue: 2,
          editRow: true,
          editRule: true,
        },
      ],
      nextStepId: 'competitionGenerate',
    },
    {
      stepId: 'competitionGenerate',
      stepTitle: '配置比赛项目',
      lastStepId: 'teamGenerate',
      formComponent: 'StepTableForm',
      formSchema: (guideResult) => [
        {
          title: 'ID',
          dataIndex: 'id',
          editRow: false,
          ifShow: false,
        },
        {
          title: '项目',
          dataIndex: 'sportEventId',
          editRow: true,
          editComponent: 'ApiSelect',
          editComponentProps: {
            api: ({ id }) => {
              return typeof id === 'string' ? apiGetSportLibSelection(id) : [];
            },
            params: {
              // @ts-ignore
              id: guideResult.get('basicInfo')?.masterOrganizationId,
            },
            labelInValue: true,
            showSearch: true,
            optionFilterProp: 'label',
          },
          editRule: true, // means required.
        },
        {
          dataIndex: 'allowedGroup',
          title: '允许的参赛组',
          editRow: true,
          editRule: true,
          editComponent: 'ApiSelect',
          defaultValue: [],
          editComponentProps: {
            api: () => {
              // @ts-ignore
              return guideResult.get('teamGroup')?.allowedGroup;
            },
            labelInValue: true,
            mode: 'multiple',
          },
          // customRender: (value) => {
          //   return value.toString();
          // },
        },
        {
          dataIndex: 'peopleGender',
          title: '性别',
          editRow: true,
          editRule: true,
          editComponent: 'ApiSelect',
          defaultValue: [],
          editComponentProps: {
            api: () => apiGetEnumSelection('people_gender'),
            labelInValue: true,
            mode: 'tags',
          },
          // customRender: (value) => {
          //   return value.toString();
          // },
        },
        {
          dataIndex: 'category',
          title: '赛制',
          editComponent: 'ApiSelect',
          editComponentProps: {
            api: () => apiGetEnumSelection('competition_category'),
            labelInValue: true,
          },
          editRow: true,
          editRule: true,
        },
        {
          dataIndex: 'peoplePerPatch',
          title: '抽签小组人数',
          placeholder: '请填写抽签小组人数',
          helpMessage: '填0则不限',
          editComponent: 'InputNumber',
          defaultValue: guideResult.get('generalSettings')?.trackNumber,
          editRow: true,
          editRule: (value) => {
            console.log(value);
            return parseInt(value) >= 0 ? '' : '人数必须大于等于0';
          },
        },
        {
          dataIndex: 'peoplePerTeam',
          title: '代表队限报',
          helpMessage: '填0则不限',
          editComponent: 'InputNumber',
          defaultValue: 2,
          editRow: true,
          editRule: true,
          customRender: ({value}) => value,
        },
      ],
    },
  ],
};

export default guideSchema;
