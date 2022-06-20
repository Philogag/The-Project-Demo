<template>

  <van-tree-select
    v-model:main-active-index="activeIndex"
    v-model:active-id="activeItemsFork"
    :items="items"
  >
    <template #content v-if="deepLevel > 2">
      <DeepTreeSelect
        :items="items[activeIndex]?.children"
        :deepLevel="deepLevel - 1"
        v-model:activeItem="activeItemsFork"
      />
    </template>
  </van-tree-select>

</template>
<script>

import { defineComponent, computed, watch, ref } from 'vue';
import { TreeSelect } from 'vant';

export default defineComponent({
  name: "DeepTreeSelect",
  components: {
    [TreeSelect.name]: TreeSelect,
  },
  model: {
    prop: 'activeItem',
    event: 'update',
  },
  props: {
    items: {type: Array, default: () => []},
    deepLevel: {type: Number, default: 2},
    activeItem: [Array, Object, String, Number],
  },
  emits: ['change-active', 'update:activeItem'],
  setup(props, { emit }) {
    const activeIndex = ref(0);
    const activeItemsFork = ref(0);

    watch(
      () => props.items, 
      () => {
        activeIndex.value = 0;
      }
    )

    watch(
      () => activeItemsFork.value,
      () => {
        emit('update:activeItem', activeItemsFork.value);
        emit('change-active');
      }
    )

    return {
      activeIndex,
      activeItemsFork,
    }
  }
})

</script>