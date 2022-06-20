import { useAppStore } from '/@/store/modules/app';
import { computed } from 'vue';

export function useAppInject() {
  // const values = useAppProviderContext();
  const appStore = useAppStore();
  
  return {
    getIsMobile: computed(() => appStore.isMobile),
  };
}
