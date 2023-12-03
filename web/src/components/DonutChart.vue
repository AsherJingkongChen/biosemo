<template>
  <svg
    version="1.1"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 200 200">
    <path
      fill="transparent"
      :d="backgroundD"
      :stroke="backgroundColor"
      :stroke-width="strokeWidthPercent" />
    <path
      fill="transparent"
      :d="foregroundD"
      :stroke="foregroundColor"
      :stroke-width="strokeWidthPercent" />
  </svg>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  percent: number;
  foregroundColor: string;
  backgroundColor: string;
  strokeWidthPercent: number;
}>();

const X = 100;
const X_2 = X / 2;
const X_APPROX = 99.9999;

const r = computed(() => X - props.strokeWidthPercent);
const y = computed(() => X - r.value);
const z = computed(() => (props.percent === X ? 'z' : ''));
const endX = computed(
  () => -Math.sin(radians.value) * r.value + X_APPROX,
);
const endY = computed(
  () => Math.cos(radians.value) * r.value + X,
);
const radians = computed(() => {
  const degrees = (props.percent / X) * 360;
  const value = degrees - 180;
  return (value * Math.PI) / 180;
});
const largeArc = computed(() => (props.percent > X_2 ? 1 : 0));
const foregroundD = computed(
  () => `\
M ${X} ${y.value} \
A ${r.value} ${r.value} \
0 ${largeArc.value} 1 \
${endX.value} ${endY.value} ${z.value}`,
);
const backgroundD = computed(
  () => `\
M ${X} ${y.value} \
A ${r.value} ${r.value} \
0 1 1 \
${X_APPROX} ${y.value} z`,
);
</script>
