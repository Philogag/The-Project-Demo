<template>
  <span :class="[prefixCls, `${prefixCls}--${theme}`]" @click="goHome">
    <HomeOutlined />
  </span>
</template>
<script lang="ts">
  import { defineComponent } from 'vue';
  import { HomeOutlined } from '@ant-design/icons-vue';
  import { useRouter } from 'vue-router';
  import { useDesign } from '/@/hooks/web/useDesign';
  import { propTypes } from '/@/utils/propTypes';

  export default defineComponent({
    name: 'HomeTrigger',
    components: { HomeOutlined },
    props: {
      theme: propTypes.oneOf(['light', 'dark']),
    },
    setup() {
      const router = useRouter();
      function goHome() {
        router.push('/dashboard');
      }

      const { prefixCls } = useDesign('layout-header-trigger');
      return { goHome, prefixCls };
    },
  });
</script>
