<template>
  <BasicDrawer
    v-bind="$attrs"
    @register="registerDrawer"
    showFooter
    title="授权菜单"
    width="30%"
    @ok="handleSubmit"
  >
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
  import { defineComponent, ref, unref } from 'vue';
  import { BasicDrawer, useDrawerInner } from '/@/components/Drawer';
  import {
    apiGetRoleMenuIdList,
    apiSetRoleMenuIdList,
    getMenuListForManager,
  } from '/@/api/system-config/menu';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { BasicTree, TreeActionType } from '/@/components/Tree';
  export default defineComponent({
    name: 'MenuSelector',
    components: { BasicDrawer, BasicTree },
    emits: ['success', 'register'],
    setup(_, { emit }) {
      const { notification } = useMessage();
      const asyncExpandTreeRef = ref<Nullable<TreeActionType>>(null);
      const treeData = ref([]);
      const checkedKeys = ref([]);
      const treeLoading = ref(false);
      const roleId = ref('');

      const build_tree = (value) => {
        return {
          title: value.title,
          key: value.id,
          icon: value.icon,
          children: value.children?.map((child) => build_tree(child)),
        };
      };

      const [registerDrawer, { setDrawerProps, closeDrawer }] = useDrawerInner(
        async ({ role_id }) => {
          roleId.value = role_id;
          treeLoading.value = true;
          let tmpTreeData = await getMenuListForManager();
          //@ts-ignore
          treeData.value = tmpTreeData.map((value) => build_tree(value));
          //@ts-ignore
          checkedKeys.value = await apiGetRoleMenuIdList(role_id);
          unref(asyncExpandTreeRef)?.expandAll(true);
          treeLoading.value = false;
        },
      );

      async function handleSubmit() {
        try {
          // console.log(checkedKeys.value)
          apiSetRoleMenuIdList({
            role_id: roleId.value,
            menu_id_list: checkedKeys.value,
          }).then((res) => {
            if (res.message.length == 0) {
              closeDrawer();
              emit('success');
            } else {
              notification.error({
                message: '错误',
                description: res.message.join('\n'),
              });
            }
          });
        } finally {
          setDrawerProps({ confirmLoading: false });
        }
      }
      return {
        registerDrawer,
        asyncExpandTreeRef,
        treeData,
        checkedKeys,
        treeLoading,
        handleSubmit,
      };
    },
  });
</script>
