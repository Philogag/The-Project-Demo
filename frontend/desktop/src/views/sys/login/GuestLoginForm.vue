<template>
  <template v-if="getShow">
    <LoginFormTitle class="enter-x" />
    <Form
      class="p-4 enter-x"
      :model="formData"
    >
      <FormItem
        name="organizationId"
        class="enter-x w-full"
      >
        <Select
          class="fix-auto-fill xl-select-w"
          size="large"
          v-model:value="formData.organizationId"
          :options="guestOrganizationOption"
          placeholder="选择访问组织"
        />
      </FormItem>
      <Button
        type="primary"
        class="enter-x"
        size="large"
        block
        @click="handleGuestLogin"
        :loading="loading"
      >
        登录为访客
      </Button>
      <Button size="large" block class="mt-4 enter-x" @click="handleBackLogin">
        {{ t('sys.login.backSignIn') }}
      </Button>
    </Form>
  </template>
</template>
<script lang="ts">
  import { defineComponent, reactive, ref, unref, computed } from 'vue';
  import LoginFormTitle from './LoginFormTitle.vue';
  import { Form, Select, Button } from 'ant-design-vue';
  import { useI18n } from '/@/hooks/web/useI18n';
  import { useLoginState, LoginStateEnum } from './useLogin';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { apiGetGuestLoginOrganizationSelection } from '/@/api/system-config/ortanization';
  import { useUserStore } from '/@/store/modules/user';

  const FormItem = Form.Item;

  export default defineComponent({
    name: 'GuestLoginForm',
    components: {
      LoginFormTitle,
      Form,
      FormItem,
      Select,
      Button,
    },
    setup() {
      const { t } = useI18n();
      const { createMessage, createNotification } = useMessage();
      const { handleBackLogin, getLoginState } = useLoginState();
      const userStore = useUserStore();

      const loading = ref(false);
      const getShow = computed(() => unref(getLoginState) === LoginStateEnum.GUEST_LOGIN);
      const formData = reactive({
        organizationId: undefined,
      });

      const guestOrganizationOption = ref([]);

      apiGetGuestLoginOrganizationSelection().then((data) => {
        //@ts-ignore
        guestOrganizationOption.value = data;
      });

      async function handleGuestLogin() {
        if (!formData.organizationId) {
          createMessage.error('请选择访问的组织', 1);
          return;
        }
        loading.value = true;
        userStore.login({
          organizationId: formData.organizationId,
          mode: 'none', // 不要默认的错误提示
          isGuest: true, // 访客模式
        }).then((userInfo) => {
          createNotification.success({
            message: t('sys.login.loginSuccessTitle'),
            description: `${t('sys.login.loginSuccessDesc')}: ${userInfo.username}`,
            duration: 3,
          });
        }).catch((error) => {
          createNotification.error({
            message: t('sys.api.errorTip'),
            description: (error as unknown as Error).message || t('sys.api.networkExceptionMsg'),
          })
        }).finally(() => {
          loading.value = false;
        })
      }

      return {
        getShow,
        formData,
        loading,
        guestOrganizationOption,
        t,
        handleBackLogin,
        handleGuestLogin,
      }
    },
  });
</script>
<style>
  @media (min-width: 1200px) {
    .xl-select-w {
      width: 404px !important;
    }
  }
</style>
