<template>
  <van-field
    v-model:modelValue="formatter"
    :is-link="!readonly"
    readonly
    :name="name"
    :label="label"
    :rules="rules"
    :placeholder="placeholder"
    @click="
      () => {
        if (!readonly) showPicker = true;
      }
    "
  />
  <van-popup v-model:show="showPicker" position="bottom">
    <van-datetime-picker
      :type="pickerType"
      :title="pickerTitle"
      :min-date="pickerMinDate"
      :max-date="pickerMaxDate"
      @confirm="handlePickerConfirm"
      @cancel="handlePickerCancel"
    />
  </van-popup>
</template>
<script>
  import { defineComponent, onMounted, ref } from 'vue';
  import { Field, Popup, DatetimePicker } from 'vant';
  import { propTypes } from '/@/utils/propTypes';
  import moment from 'moment';
  export default defineComponent({
    name: 'PopupDatetimePickerField',
    components: {
      [Field.name]: Field,
      [Popup.name]: Popup,
      [DatetimePicker.name]: DatetimePicker,
    },
    model: {
      prop: 'value',
      event: 'update:value',
    },
    props: {
      //// For Field
      value: [String, Date],
      name: propTypes.string.def('datetime'),
      label: propTypes.string.def(''),
      placeholder: propTypes.string.def('请选择'),
      format: propTypes.string.def('YYYY 年 M 月 D 日'),
      rules: Array,
      readonly: propTypes.bool.def(false),
      //// For Picker
      pickerType: propTypes.string.def('date'),
      pickerTitle: propTypes.string.def('请选择日期'),
      pickerMinDate: {
        type: Date,
        default: () => new Date(),
      },
      pickerMaxDate: {
        type: Date,
        default: () => new Date(),
      },
    },
    emits: ['confirm', 'cancel', 'update:value'],
    setup(props, { emit }) {
      const showPicker = ref(false);
      const valueFork = ref(null);

      function handlePickerConfirm(date) {
        // console.log(date);
        valueFork.value = date;
        emit('update:value', date);
        emit('confirm', date);
        showPicker.value = false;
      }

      function handlePickerCancel() {
        emit('cancel');
        showPicker.value = false;
      }

      onMounted(() => {
        valueFork.value = props.value;
      });

      return {
        valueFork,
        showPicker,
        handlePickerConfirm,
        handlePickerCancel,
      };
    },
    computed: {
      formatter() {
        return this.valueFork ? moment(this.valueFork).format(this.$props.format) : '';
      },
    },
  });
</script>
