export const stepBasicFormProps = {
  schemas: {
    type: Array,
    default: () => [],
  },
  data: {
    type: Object,
    default: () => ({}),
  },
};

export const stepTableFormProps = {
  schemas: {
    type: Array,
    default: () => [],
  },
  data: {
    type: Array as PropType<Recordable[]>,
    default: null,
  },
};
