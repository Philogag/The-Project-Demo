<template>
  <BasicDrawer
    v-bind="$attrs"
    @register="registerDrawer"
    showFooter
    :title="title"
    width="30%"
    @ok="handleSubmit"
  >
    <template #insertFooter>
      <PopConfirmButton
        title="即将清空授权，请再次确认"
        placement="topRight"
        @confirm="handleClearRoutes"
        >清空授权
      </PopConfirmButton>
    </template>
    <Spin :spinning="treeLoading">
      <BasicTree
        :treeData="treeData"
        v-model:checkedKeys="checkedKeys"
        :checkable="true"
        ref="asyncExpandTreeRef"
      />
    </Spin>
  </BasicDrawer>
</template>
<script lang="ts">
  import { computed, defineComponent, ref, unref } from 'vue';
  import { Spin } from 'ant-design-vue';
  import { BasicDrawer, useDrawerInner } from '/@/components/Drawer';
  import {
    apiClearMenuDataRouteIdList,
    apiGetMenuDataRouteIdList,
    apiSetMenuDataRouteIdList
  } from '/@/api/system-config/menu';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { BasicTree, TreeActionType } from '/@/components/Tree';
  import { apiGetDataRouteSelection } from '/@/api/system-config/route';
  import { PopConfirmButton } from '/@/components/Button';
  export default defineComponent({
    name: 'MenuSelector',
    components: { BasicDrawer, BasicTree, Spin, PopConfirmButton },
    emits: ['success', 'register'],
    setup(_, { emit }) {
      const { notification } = useMessage();
      const asyncExpandTreeRef = ref<Nullable<TreeActionType>>(null);
      const treeData = ref([]);
      const checkedKeys = ref([]);
      const treeLoading = ref(false);
      const menuId = ref('');
      const menuTitle = ref('');
      const title = computed(() => '授权菜单 - ' + unref(menuTitle));

      const build_tree = (value) => {
        return {
          title: value.label,
          key: value.value,
          children: value.children?.map((child) => build_tree(child)),
        };
      };

      const reload = async () => {
        treeLoading.value = true;
        //@ts-ignore
        checkedKeys.value = await apiGetMenuDataRouteIdList(menuId.value);
        treeLoading.value = false;
      };

      const [registerDrawer, { setDrawerProps, closeDrawer }] = useDrawerInner(
        async ({ menu_id, menu_title }) => {
          menuId.value = menu_id;
          menuTitle.value = menu_title;
          let tmpTreeData = await apiGetDataRouteSelection();
          //@ts-ignore
          treeData.value = tmpTreeData.map((value) => build_tree(value));
          await reload();
          setDrawerProps({ confirmLoading: false });
        },
      );

      async function handleSubmit() {
        setDrawerProps({ confirmLoading: true });
        await apiSetMenuDataRouteIdList({
          menuId: menuId.value,
          routeIdList: checkedKeys.value,
        }).then(() => {
          closeDrawer();
          emit('success');
        });
        setDrawerProps({ confirmLoading: false });
      }

      async function handleClearRoutes() {
        treeLoading.value = true;
        await apiClearMenuDataRouteIdList(menuId.value).then(() => {
          reload();
          emit('success');
        });
        treeLoading.value = false;
      }

      return {
        title,
        registerDrawer,
        asyncExpandTreeRef,
        treeData,
        checkedKeys,
        treeLoading,
        handleSubmit,
        handleClearRoutes,
      };
    },
  });
</script>
