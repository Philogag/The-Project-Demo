<template>
  <Dropdown
    placement="bottomLeft"
    :overlayClassName="`${prefixCls}-dropdown-overlay`"
    :trigger="['click']"
  >
    <span :class="[prefixCls, `${prefixCls}--${theme}`]" class="flex">
      <img :class="`${prefixCls}__header`" :src="getUserInfo.avatar" />
      <span :class="`${prefixCls}__info hidden md:block`">
        <span :class="`${prefixCls}__name  `" class="truncate">
          <template v-if="getUserInfo.currentRole.code === 'guest'">
            访客模式
          </template>
          <template v-else>
            {{ getUserInfo.realName }} | {{ getUserInfo.currentRole.roleName }}
          </template>
        </span>
      </span>
    </span>

    <template #overlay>
      <Menu @click="handleMenuClick">
        <div v-if="getUserRoles">
          <MenuItem
            v-for="item in getUserInfo.roles"
            :key="'role-' + item.id"
            :text="item.roleName"
            icon="ant-design:team-outlined"
          />
          <MenuDivider />
        </div>
        <MenuItem
          key="doc"
          :text="t('layout.header.dropdownItemDoc')"
          icon="ion:document-text-outline"
          v-if="getShowDoc"
        />
        <MenuDivider v-if="getShowDoc" />
        <!--        <MenuItem-->
        <!--          v-if="getUseLockPage"-->
        <!--          key="lock"-->
        <!--          :text="t('layout.header.tooltipLock')"-->
        <!--          icon="ion:lock-closed-outline"-->
        <!--        />-->
        <!-- <MenuItem
          key="reset-password"
          text="修改密码"
          icon="ant-design:unlock-outlined"
        /> -->
        <MenuItem
          key="logout"
          :text="t('layout.header.dropdownItemLoginOut')"
          icon="ion:power-outline"
        />
      </Menu>
    </template>
  </Dropdown>
  <LockAction @register="register" />
  <!-- <SetPasswordModal v-model:visible="doSetPassword" /> -->
</template>
<script lang="ts">
  // components
  import { Dropdown, Menu } from 'ant-design-vue';

  import { defineComponent, computed, ref } from 'vue';

  import { DOC_URL } from '/@/settings/siteSetting';

  import { useUserStore } from '/@/store/modules/user';
  import { useHeaderSetting } from '/@/hooks/setting/useHeaderSetting';
  import { useI18n } from '/@/hooks/web/useI18n';
  import { useDesign } from '/@/hooks/web/useDesign';
  import { useModal } from '/@/components/Modal';

  import headerImg from '/@/assets/images/header.jpg';
  import { propTypes } from '/@/utils/propTypes';
  import { openWindow } from '/@/utils';

  import { createAsyncComponent } from '/@/utils/factory/createAsyncComponent';
  import { apiSwitchCurrentRole } from '/@/api/system-config/role';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { usePermission } from '/@/hooks/web/usePermission';

  type MenuEvent = 'logout' | 'doc' | 'lock' | 'reset-password';

  export default defineComponent({
    name: 'UserDropdown',
    components: {
      Dropdown,
      Menu,
      MenuItem: createAsyncComponent(() => import('./DropMenuItem.vue')),
      MenuDivider: Menu.Divider,
      LockAction: createAsyncComponent(() => import('../lock/LockModal.vue')),
      // SetPasswordModal: createAsyncComponent(() => import('../../../modal/set-password/SetPasswordModal.vue')),
    },
    props: {
      theme: propTypes.oneOf(['dark', 'light']),
    },
    setup() {
      const { prefixCls } = useDesign('header-user-dropdown');
      const { t } = useI18n();
      const { getShowDoc, getUseLockPage } = useHeaderSetting();
      const userStore = useUserStore();
      const { refreshMenu } = usePermission();
      const { notification } = useMessage();

      const getUserInfo = computed(() => {
        const {
          username: realName,
          avatar,
          desc,
          roles,
          currentRole,
        } = userStore.getUserInfo || {};
        return { realName, avatar: avatar || headerImg, desc, roles, currentRole };
      });

      const getUserRoles = true;

      const [register, { openModal }] = useModal();

      function handleLock() {
        openModal(true);
      }

      //  login out
      function handleLoginOut() {
        userStore.confirmLoginOut();
      }

      // open doc
      function openDoc() {
        openWindow(DOC_URL);
      }

      const doSetPassword = ref(false);
      function openSetPassword() {
        doSetPassword.value = true;
      }

      function switchCurrentRole(role_id: string) {
        apiSwitchCurrentRole(role_id).then(async (res) => {
          userStore.resetUserInfo();
          await userStore.afterLoginAction(true);
          await refreshMenu();
          console.log(`Switch to role: ${role_id}`);
        });
      }

      function handleMenuClick(e: { key: MenuEvent }) {
        switch (e.key) {
          case 'logout':
            handleLoginOut();
            break;
          case 'doc':
            openDoc();
            break;
          case 'lock':
            handleLock();
            break;
          case 'reset-password':
            openSetPassword();
            break;
        }

        if (e.key.startsWith('role')) {
          switchCurrentRole(e.key.substr(5));
        }
      }

      return {
        prefixCls,
        t,
        getUserInfo,
        handleMenuClick,
        getShowDoc,
        getUserRoles,
        register,
        getUseLockPage,
        doSetPassword,
      };
    },
  });
</script>
<style lang="less">
  @prefix-cls: ~'@{namespace}-header-user-dropdown';

  .@{prefix-cls} {
    height: @header-height;
    padding: 0 0 0 10px;
    padding-right: 10px;
    overflow: hidden;
    font-size: 12px;
    cursor: pointer;
    align-items: center;

    img {
      width: 24px;
      height: 24px;
      margin-right: 12px;
    }

    &__header {
      border-radius: 50%;
    }

    &__name {
      font-size: 14px;
    }

    &--dark {
      &:hover {
        background-color: @header-dark-bg-hover-color;
      }
    }

    &--light {
      &:hover {
        background-color: @header-light-bg-hover-color;
      }

      .@{prefix-cls}__name {
        color: @text-color-base;
      }

      .@{prefix-cls}__desc {
        color: @header-light-desc-color;
      }
    }

    &-dropdown-overlay {
      .ant-dropdown-menu-item {
        min-width: 160px;
      }
    }
  }
</style>
