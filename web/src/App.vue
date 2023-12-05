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
        <div class="mono-counsel-card-list-scroller">
          <div
            class="mono-counsel-card-list"
            ref="listElem"
            v-auto-scroll-down>
            <MonoCounselCard
              v-for="(item, index) in monoCounselsStore"
              :key="index"
              :percent="item.percent"
              :text="item.text"
              ref="" />
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<script setup lang="ts">
import DonutChart from '@/components/DonutChart.vue';
import MonoCounselCard from '@/components/MonoCounselCard.vue';
import { computed, ref, watch } from 'vue';
import {
  useEmoLevelStore,
  useMonoCounselsStore,
} from '@/stores';
import { vAutoScrollDown } from '@/utils';

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
const monoCounselsStore = useMonoCounselsStore();

// watcher

// interval in ticks
const MONO_COUNSEL_INTERVAL = 1000;
let emoPercentWindow: number[] = [];

watch(
  () => emoLevelStore.tick,
  async (tick) => {
    if (tick !== undefined) {
      emoPercentWindow.push(emoLevelStore.percent);
      if (emoPercentWindow.length > MONO_COUNSEL_INTERVAL) {
        emoPercentWindow.shift();
      }

      if (tick % MONO_COUNSEL_INTERVAL === 0) {
        const emoPercentMean =
          emoPercentWindow.reduce((acc, cur) => acc + cur, 0) /
          emoPercentWindow.length;
        const emoPercentMeanExtended =
          emoLevelStore.percent * 0.25 + emoPercentMean * 0.75;

        await monoCounselsStore.push({
          category: emoLevelStore.category,
          highPercent: emoLevelStore.highPercent,
          percent: emoPercentMeanExtended,
        });
      }
    } else {
      emoPercentWindow = [];
    }
  },
);

// callbacks

async function onChangeEmoLevelFileInputElem() {
  const file = emoLevelFileInputElem?.value?.files?.[0];
  if (file) {
    if (isEmoLevelFileInputElemLocked.value) {
      throw new Error('The file input element is locked now');
    }

    // init state
    isEmoLevelFileInputElemLocked.value = true;
    monoCounselsStore.$reset();

    emoLevelStore
      .getLevels(file)
      .catch((e) => {
        alert(
          `Failed to get emotion levels from the file:\n${e}`,
        );
      })
      .finally(() => {
        // reset state
        isEmoLevelFileInputElemLocked.value = false;
        emoLevelStore.$reset();
      });
  }
}
</script>

<style scoped lang="scss">
@use 'sass:math';
@import '@/assets/base.scss';

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
      $BUTTON_PADDING_BLOCK: 0.25em;
      $BUTTON_PADDING_INLINE: 1em;
      $BUTTON_BORDER_RADIUS: 1em * $LINE_HEIGHT + 2 *
        $BUTTON_PADDING_BLOCK;
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: center;
      gap: 1.5em;
      position: relative;
      width: 100%;
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
        background-color: var(--color-background-soft);
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
          background-color: var(--vt-c-turquoise);
          color: var(--color-background);
        }
        &.locked {
          &,
          * {
            cursor: not-allowed;
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
  .mono-counsel-card-list-scroller {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    width: 100%;
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
  .mono-counsel-card-list {
    $CHAT_CARD_PADDING: 1em;
    position: relative;
    overflow-x: hidden;
    overflow-y: scroll;
    display: flex;
    flex-direction: column;
    position: relative;
    min-height: 35vh;
    width: 85%;
    max-height: 35vh;
    background-color: var(--color-background-soft);
    border: thin solid var(--color-border);
    border-radius: $BORDER_RADIUS;
    padding: math.div($CHAT_CARD_PADDING, 2);
    // .mono-counsel-card-item {
    //   position: relative;
    //   width: 100%;
    // }
  }
}
</style>
