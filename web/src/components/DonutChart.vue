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
import { computed } from '@vue/reactivity';

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
const largeArc = computed(() =>
  props.percent < X_2 ? 0 : 1,
);
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

// Vue.component('donut-chart', {
//   props: ['percent', 'foreground-color', 'background-color',
//          'stroke-width', 'radius'],
//   template: '#donut-template',
//   replace: true,
//   data: function () {
//     return {
//       // default values
//       foregroundColor: "#badaff",
//       backgroundColor: "#bada55",
//       radius: 85,
//       strokeWidthPercent: 20,
//       percent: 25
//     }
//   },
//   computed: {
//     // If more than 50% filled we need to switch arc drawing mode from less than 180 deg to more than 180 deg
//     largeArc: function () {
//       return this.percent < 50 ? 0 : 1;
//     },
//     // Where to put x coordinate of center of circle
//     x: function () {
//       return 100;
//     },
//     // Where to put y coordinate of center of circle
//     y: function () {
//       return 100 - this.radius;
//     },
//     // Calculate X coordinate of end of arc (+ 100 to move it to middle of image)
//     // add some rounding error to make arc not disappear at 100%
//     endX: function () {
//       return -Math.sin(this.radians) * this.radius + 100 - 0.0001;
//     },
//     // Calculate Y coordinate of end of arc (+ 100 to move it to middle of image)
//     endY: function () {
//       return Math.cos(this.radians) * this.radius + 100;
//     },
//     // Calculate length of arc in radians
//     radians: function () {
//       var degrees = (this.percent/100)*360
//       var value = degrees - 180; // Turn the circle 180 degrees counter clockwise

//       return (value*Math.PI)/180;
//     },
//     // If we reach full circle we need to complete the circle, this ties into the rounding error in X coordinate above
//     z: function () {
//       return this.percent == 100 ? 'z' : '';
//     },
//     dBg: function () {
//       return "M "+this.x+" "+this.y+" A "+this.radius+" "+this.radius+" 0 1 1 "+(this.x-0.0001)+" "+this.y+" z";
//     },
//     d: function () {
//       return "M "+this.x+" "+this.y+" A "+this.radius+" "+this.radius+" 0 "+this.largeArc+" 1 "+this.endX+" "+this.endY+" "+this.z;
//     }
//   }
// });
</script>

<style scoped lang="scss"></style>
