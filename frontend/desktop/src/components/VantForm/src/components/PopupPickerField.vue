<template>
  <div>
    <van-field
      v-model="valueFork"
      :formatter="formatter"
      :is-link="!readonly"
      readonly
      :name="name"
      :label="label"
      :placeholder="placeholder"
      :rules="rules"
      @click="handleBeforeClick"
    />
    <van-popup v-model:show="showPicker" position="bottom">
      <van-picker
        :title="pickerTitle"
        :columns="realOptions"
        :columns-field-names="{
          text: optionLabelKey,
          children: optionChildrenKey,
        }"
        @confirm="handlePickerConfirm"
        @cancel="handlePickerCancel"
      />
    </van-popup>
  </div>
</template>
<script>
  import { defineComponent, onMounted, ref, watch } from 'vue';
  import { Field, Popup, Picker } from 'vant';
  import { propTypes } from '/@/utils/propTypes';
  import { get } from 'lodash-es';
  import { isFunction } from '/@/utils/is';
  export default defineComponent({
    name: 'PopupPickerField',
    components: {
      [Field.name]: Field,
      [Popup.name]: Popup,
      [Picker.name]: Picker,
    },
    model: {
      prop: 'value',
      event: 'change',
    },
    props: {
      //// For Field
      value: [Array, Object, String, Number],
      name: propTypes.string.def('picker'),
      label: propTypes.string.def(''),
      placeholder: propTypes.string.def('请选择'),
      rules: Array,
      readonly: propTypes.bool.def(false),
      autoFirst: propTypes.bool.def(false),
      //// For Picker
      pickerTitle: propTypes.string.def('请选择'),
      options: {
        type: Array,
        default: () => [],
      },
      optionValueKey: propTypes.string.def('value'),
      optionLabelKey: propTypes.string.def('label'),
      optionChildrenKey: propTypes.string.def('children'),
    },
    emits: ['click', 'confirm', 'cancel', 'update:value'],
    setup(props, { emit }) {
      const showPicker = ref(false);
      const valueFork = ref('');
      const realOptions = ref([]);

      function handleBeforeClick() {
        emit('click');
        if (!props.readonly) showPicker.value = true;
      }

      function handlePickerConfirm(selected) {
        valueFork.value = get(selected, props.optionValueKey) || selected;
        emit('update:value', valueFork.value);
        emit('confirm', valueFork.value, selected);
        showPicker.value = false;
      }

      function handlePickerCancel() {
        emit('cancel');
        showPicker.value = false;
      }

      async function fetchOptions() {
        if (isFunction(props.options)) {
          realOptions.value = await props.options();
        } else {
          realOptions.value = props.options;
        }
        if (props.autoFirst && !props.value && realOptions.value.length > 0) {
          valueFork.value = get(realOptions.value[0], props.optionValueKey)
          emit('update:value', valueFork.value);
        }
      }


      watch(() => props.options, fetchOptions);
      
      onMounted(async () => {
        await fetchOptions();
        valueFork.value = props.value ? props.value : valueFork.value;
      });

      const formatter = (value) => {
        const options = realOptions.value.filter((o) => (get(o, props.optionValueKey) || o) === value);
        // console.log(value, options, realOptions);
        return options.length > 0 ? get(options[0], props.optionLabelKey) || options[0] : value;
      };
      return {
        valueFork,
        realOptions,
        showPicker,
        formatter,
        handleBeforeClick,
        handlePickerConfirm,
        handlePickerCancel,
      };
    },
  });
</script>
