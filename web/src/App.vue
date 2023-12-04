<template>
  <header></header>
  <main>
    <div class="background">
      <section class="u-">
        <section class="a--">
          <DonutChart
            class="emo-percent-chart"
            :percent="emoLevelStore.percent"
            :foreground-color="emoLevelStore.color"
            background-color="var(--color-border)"
            :stroke-width-percent="15" />
          <div class="emo-percent">
            {{ emoLevelStore.percentRounded }}%
          </div>
        </section>
        <section class="b--">
          <div class="cabinet">
            <section class="emo-status">
              <div class="emo-category">
                {{ emoLevelStore.categoryCapped }}
              </div>
              <div
                class="emo-label"
                :style="{
                  color: emoLevelStore.color,
                }">
                {{ emoLevelStore.label }}
              </div>
            </section>
            <section
              class="emo-level-file"
              :class="{
                locked: isEmoLevelFileInputElemLocked,
              }">
              <div
                class="emo-level-file-heading"
                @click="
                  if (!isEmoLevelFileInputElemLocked) {
                    emoLevelFileInputElem?.click();
                  }
                ">
                {{ emoLevelFileHeading }}
              </div>
              <input
                type="file"
                id="emo-level-file-input"
                accept="application/json, .json"
                ref="emoLevelFileInputElem"
                @change="onChangeEmoLevelFileInputElem"
                hidden />
            </section>
          </div>
        </section>
      </section>
      <section class="b-">
        <div class="scroll-view">
          <div class="scroll-target mono-consult-card-list">
            <MonoConsultCard
              v-for="(percent, index) in [29, 37, 53, 71, 97]"
              :key="index"
              :percent="percent"
              text="
Ok, I will try to help you.
Can you tell me what happened?
Nevermind, I will try to help you." />
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<script setup lang="ts">
import DonutChart from '@/components/DonutChart.vue';
import MonoConsultCard from './components/MonoConsultCard.vue';
import { computed, ref, watch } from 'vue';
import { useEmoLevelStore, useMonoConsultStore } from './stores';

// ref

const emoLevelFileInputElem = ref<
  HTMLInputElement | undefined
>();
const isEmoLevelFileInputElemLocked = ref(false);

// computed

const emoLevelFileHeading = computed(() => {
  if (!isEmoLevelFileInputElemLocked.value) {
    return 'Upload File';
  } else {
    const progress = emoLevelStore.length
      ? Math.round(
          ((emoLevelStore.tick ?? 0) / emoLevelStore.length) *
            100,
        )
      : '?';
    return `Running ${progress}%`;
  }
});

// store

const emoLevelStore = useEmoLevelStore();
const monoConsultStores: ReturnType<
  typeof useMonoConsultStore
>[] = [];

// wather

// watch(
//   () => emoLevelStore.tick,
//   (tick) => {
//     if (tick === undefined)
//   },
// );

// functions

async function onChangeEmoLevelFileInputElem() {
  const file = emoLevelFileInputElem?.value?.files?.[0];
  if (!file) {
    console.debug('Cancelled uploading file');
    return;
  }

  if (isEmoLevelFileInputElemLocked.value) {
    throw new Error('The file input element is locked now');
  }
  isEmoLevelFileInputElemLocked.value = true;

  await emoLevelStore
    .getLevels(file)
    .catch((e) => {
      alert(`Failed to get emotion levels from the file:\n${e}`);
    })
    .finally(() => {
      isEmoLevelFileInputElemLocked.value = false;
      emoLevelStore.$reset();
      console.warn('emoLevelStore.$reset is disabled');
    });
}
</script>

<style scoped lang="scss">
@use 'sass:math';
@import './assets/base.css';

.background {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 100%;
}
.u- {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  width: 100%;
  .a-- {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    width: 25%;
    min-width: 10em;
    .emo-percent-chart {
      position: relative;
      width: 100%;
    }
    .emo-percent {
      display: grid;
      place-items: center;
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      font-size: 2em;
      color: var(--color-heading);
    }
  }
  .b-- {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    width: 100%;
    padding-block: 1.5em;
    .cabinet {
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: center;
      gap: 1.5em;
      position: relative;
      width: 100%;
      $BUTTON_PADDING_BLOCK: 0.25em;
      $BUTTON_PADDING_INLINE: 1em;
      $BUTTON_BORDER_RADIUS: calc(
        var(--line-height) * 1em + 2 * $BUTTON_PADDING_BLOCK
      );
      text-align: center;
      .emo-status {
        $LABEL_TEXT_MAX_CHARS: 7 + 1;
        $LABEL_VALUE_MAX_CHARS: 9 + 1;
        display: flex;
        flex-direction: row;
        align-items: center;
        position: relative;
        border: thin solid var(--color-border);
        border-radius: $BUTTON_BORDER_RADIUS;
        > * {
          padding: $BUTTON_PADDING_BLOCK $BUTTON_PADDING_INLINE;
          min-height: $BUTTON_BORDER_RADIUS;
        }
        .emo-category {
          border-right: thin solid var(--color-border);
          color: var(--color-heading);
          min-width: 2 * $BUTTON_PADDING_INLINE + 0.5 *
            $LABEL_TEXT_MAX_CHARS;
        }
        .emo-label {
          min-width: 2 * $BUTTON_PADDING_INLINE + 0.5 *
            $LABEL_VALUE_MAX_CHARS;
          font-weight: bold;
          text-shadow:
            1px 1px 0 var(--color-border),
            1px 0px 0 var(--color-border);
        }
      }
      .emo-level-file {
        position: relative;
        border: thin solid transparent;
        border-radius: $BUTTON_BORDER_RADIUS;
        padding: $BUTTON_PADDING_BLOCK $BUTTON_PADDING_INLINE;
        transition: 0.15s linear;
        &:hover {
          filter: brightness(0.75);
        }
        & {
          &,
          * {
            cursor: pointer;
          }
          background-color: var(--color-turquoise);
          color: var(--color-background);
        }
        &.locked {
          &,
          * {
            cursor: wait;
          }
          background-color: var(--color-border);
          color: var(--color-heading);
        }
        .emo-level-file-heading {
          min-width: 6em + 0.5;
          user-select: none;
        }
      }
    }
  }
}
.b- {
  $BORDER_RADIUS: 0.25em;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  width: 100%;
  .scroll-view {
    display: flex;
    flex-direction: column;
    position: relative;
    width: 100%;
    .scroll-target {
      position: relative;
      width: 100%;
      overflow-x: hidden;
      overflow-y: scroll;
    }
    ::-webkit-scrollbar {
      display: block;
      width: $BORDER_RADIUS;
    }
    ::-webkit-scrollbar-track {
      width: 2 * $BORDER_RADIUS;
    }
    ::-webkit-scrollbar-thumb {
      border-radius: 2 * $BORDER_RADIUS;
      background-color: var(--color-border-hover);
    }
  }
  .mono-consult-card-list {
    $CHAT_CARD_PADDING: 1em;
    display: flex;
    flex-direction: column;
    position: relative;
    min-height: calc(
      var(--line-height) * 5em + 3 * $CHAT_CARD_PADDING + 4px
    );
    max-height: 50vh;
    background-color: var(--color-background-soft);
    border: thin solid var(--color-border);
    border-radius: $BORDER_RADIUS;
    padding: math.div($CHAT_CARD_PADDING, 2);
  }
}
</style>
