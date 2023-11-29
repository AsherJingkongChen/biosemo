<template>
  <div :style="{ background }"></div>
</template>

<script setup lang="ts">
import { stressPercentColorMap } from '@/utils';
import { computed } from '@vue/reactivity';

const props = defineProps<{
  percent: number;
}>();

const background = computed(() => {
  const colors = [
    stressPercentColorMap(props.percent, 1.0),
    stressPercentColorMap(props.percent, 0.5),
    stressPercentColorMap(props.percent, 0.25),
  ];
  return `\
linear-gradient(\
to bottom, \
${colors[0]} 0em, \
${colors[1]} 5em, \
${colors[2]} 10em)`;
});
</script>

<style scoped lang="scss"></style>
