<template>
  <div :style="{ background }"></div>
</template>

<script setup lang="ts">
import { percentColorMap_RYG } from '@/utils';
import { computed } from 'vue';

const props = defineProps<{
  percent: number;
}>();

const background = computed(() => {
  const colors = [
    percentColorMap_RYG(props.percent, 1.0),
    percentColorMap_RYG(props.percent, 0.5),
    percentColorMap_RYG(props.percent, 0.25),
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
