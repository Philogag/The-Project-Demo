<template>
  <Card :title="title" v-bind="$attrs">
    <template v-for="item in items" :key="item">
      <CardGrid @click="() => {goPath(item?.route)}">
        <span class="flex flex-col items-center">
          <Icon :icon="item.icon" :color="item.color" size="20" />
          <span class="text-md mt-2">{{ item.title }}</span>
        </span>
      </CardGrid>
    </template>
  </Card>
</template>
<script lang="ts">
  import { defineComponent } from 'vue';
  import { useRouter } from 'vue-router';
  import { Card } from 'ant-design-vue';
  import { Icon } from '/@/components/Icon';
  import {quickNavProps} from './types/props';

  const CardGrid = Card.Grid;
  export default defineComponent({
    name: 'QuickNav',
    components:{
      Card,
      CardGrid,
      Icon,
    },
    props: quickNavProps,
    setup (porps) {
      const router = useRouter();

      function goPath(route) {
        if (route) router.push(route);
      }

      return {
        goPath
      }
    }
  })
</script>
