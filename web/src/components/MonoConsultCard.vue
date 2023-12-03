<template>
  <div class="mono-consult-card-item">
    <EmoLevelRibbon
      class="emo-level-ribbon"
      :percent="percent" />
    <div
      class="mono-consult-text"
      v-html="markedText"></div>
  </div>
</template>

<script setup lang="ts">
import EmoLevelRibbon from './EmoLevelRibbon.vue';
import { marked } from 'marked';
import { computed } from 'vue';

const props = defineProps<{
  percent: number;
  text: string;
}>();

const markedText = computed(() => {
  return marked(props.text, {
    async: false,
    breaks: true,
  }) as string;
});
</script>

<style scoped lang="scss">
.mono-consult-card-item {
  display: flex;
  flex-direction: row;
  gap: 1em;
  position: relative;
  width: 100%;
  padding: 1em;
  .emo-level-ribbon {
    position: relative;
    width: 0.25em;
    background: linear-gradient(
      to bottom,
      var(--color-border) 0em,
      var(--color-background-mute) 5em,
      var(--color-background-soft) 10em
    );
  }
  .mono-consult-text {
    position: relative;
    word-break: break-word;
    // white-space: pre-wrap;
  }
}
</style>
