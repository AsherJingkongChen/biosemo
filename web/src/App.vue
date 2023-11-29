<template>
  <header></header>

  <main>
    <div class="background">
      <section class="u-">
        <section class="a--">
          <DonutChart
            class="donut-chart"
            :percent="meanStressPercent"
            :foreground-color="stressColor"
            background-color="var(--color-border)"
            :stroke-width-percent="15" />
          <div class="donut-chart-percent">
            {{ meanStressPercent }}%
          </div>
        </section>
        <section class="b--">
          <div class="cabinet">
            <section class="a---">
              <div class="text text-stress-level">
                Stress Level
              </div>
              <div
                class="stress-label"
                :style="{
                  color: stressColor,
                }">
                {{ stressLabel }}
              </div>
            </section>
            <section class="b---">
              <div class="upload-file">Upload</div>
            </section>
          </div>
        </section>
      </section>
      <section class="b-">
        <div class="scroll-view">
          <div class="scroll-target chat-card-list">
            <div
              class="chat-card-item"
              key="0">
              <StressRibbon
                class="stress-ribbon"
                :percent="25" />
              <div class="chat-info">
                了解，壓力很大的時候可以嘗試以下幾種方法來幫助自己紓壓：
                <br /><br />
                1.
                深呼吸：專注地深呼吸可以幫助你放鬆身心。慢慢吸氣，然後再慢慢吐氣，並專注於呼吸的感覺，將注意力從壓力上轉移開來。
                <br /><br />
                2.
                運動：運動釋放出內啡肽，這是一種能夠讓你感到快樂和放鬆的天然化學物質。試試散步、跑步、瑜伽等活動，讓身體活動起來，減輕壓力。
                <br /><br />
                3.
                與他人交流：和朋友、家人或專業人士分享你的感受和困擾。有人傾聽和理解你的感受可以減輕壓力，並可能提供有用的建議和支持。
                <br /><br />
                4.
                時間管理：好的時間管理可以幫助你更有效地處理壓力。確定優先事項，制定一個計劃，合理分配時間，並為自己留出一些休息和放鬆的時間。
                <br /><br />
                5.
                飲食和睡眠：保持均衡的飲食和良好的睡眠習慣對於減輕壓力非常重要。嘗試避免過多的咖啡因和糖分，並確保每晚獲得充足的睡眠。
                <br /><br />
                6.
                創造性活動：找一個可以讓你放鬆和發洩的創造性活動，例如繪畫、寫作、唱歌等。這些活動可以轉移注意力，幫助你釋放壓力。
                <br /><br />
                如果你覺得壓力無法自行緩解，或者壓力對你的日常生活造成了嚴重的困擾，建議尋求專業的心理輔導或醫療支持。
              </div>
            </div>
            <div
              class="chat-card-item"
              key="1">
              <StressRibbon
                class="stress-ribbon"
                :percent="73" />
              <div class="chat-info">
                1.
                深呼吸：專注深呼吸轉移注意力，紓解壓力。<br />
                2.
                運動：釋放內啡肽，嘗試散步、跑步等活動減輕壓力。<br />
                3.
                交流：與朋友、家人分享感受，獲得支持和建議。<br />
                4.
                時間管理：有效處理壓力，合理安排休息時間。<br />
                5.
                飲食與睡眠：均衡飲食、充足睡眠對減輕壓力有幫助。<br />
                6.
                創造性活動：嘗試繪畫、寫作等活動轉移注意力。<br />
                7.
                專業支持：如壓力難以緩解，建議尋求心理輔導或醫療支持。<br />
              </div>
            </div>
            <div
              class="chat-card-item"
              key="2">
              <StressRibbon
                class="stress-ribbon"
                :percent="35" />
              <div class="chat-info">
                1.
                <strong>深呼吸：</strong
                >專注慢慢的深呼吸，有助於放鬆身心，轉移注意力。
                <br /><br />
                2.
                <strong>運動：</strong
                >散步、跑步或瑜伽能釋放內啡肽，提升心情，減輕壓力感。
                <br /><br />
                3.
                <strong>交流：</strong
                >與朋友或家人分享感受，得到支持和理解，減輕心理負擔。
                <br /><br />
                4.
                <strong>時間管理：</strong
                >制定合理的計劃，優先處理事務，保留時間給自己休息。
                <br /><br />
                5.
                <strong>飲食與睡眠：</strong
                >維持均衡飲食，確保充足睡眠，對身心健康有益。
                <br /><br />
                6.
                <strong>創造性活動：</strong
                >嘗試讓自己沈浸在創造性活動中，如繪畫或寫作，轉移注意力，紓解壓力。
                <br /><br />
                7.
                <strong>冥想與放鬆技巧：</strong
                >學習冥想或放鬆技巧，有助於提升心理靈活性，減輕緊張感。
                <br /><br />
                8.
                <strong>尋求專業支持：</strong
                >如果壓力難以自行緩解，考慮尋求心理輔導或醫療支持，專業幫助能提供有效的解決方案。
              </div>
            </div>
            <div
              class="chat-card-item"
              key="3">
              <StressRibbon
                class="stress-ribbon"
                :percent="60" />
              <div class="chat-info">
                Ok, I will try to help you. Can you tell me
                what happened? Nevermind, I will try to help
                you. Can you tell me what happened?
              </div>
            </div>
            <div
              class="chat-card-item"
              key="4">
              <StressRibbon
                class="stress-ribbon"
                :percent="60" />
              <div class="chat-info">
                Ok, I will try to help you. Can you tell me
                what happened? Nevermind, I will try to help
                you. Can you tell me what happened?
              </div>
            </div>
            <div
              class="chat-card-item"
              key="5">
              <StressRibbon
                class="stress-ribbon"
                :percent="86" />
              <div class="chat-info">
                1.
                深呼吸：專注深呼吸轉移注意力，紓解壓力。<br />
                2.
                運動：釋放內啡肽，嘗試散步、跑步等活動減輕壓力。<br />
                3.
                交流：與朋友、家人分享感受，獲得支持和建議。<br />
                4.
                時間管理：有效處理壓力，合理安排休息時間。<br />
                5.
                飲食與睡眠：均衡飲食、充足睡眠對減輕壓力有幫助。<br />
                6.
                創造性活動：嘗試繪畫、寫作等活動轉移注意力。<br />
                7.
                專業支持：如壓力難以緩解，建議尋求心理輔導或醫療支持。<br />
              </div>
            </div>
            <div
              class="chat-card-item"
              key="6">
              <StressRibbon
                class="stress-ribbon"
                :percent="29" />
              <div class="chat-info">
                1.
                <strong>深呼吸：</strong
                >專注慢慢的深呼吸，有助於放鬆身心，轉移注意力。
                <br /><br />
                2.
                <strong>運動：</strong
                >散步、跑步或瑜伽能釋放內啡肽，提升心情，減輕壓力感。
                <br /><br />
                3.
                <strong>交流：</strong
                >與朋友或家人分享感受，得到支持和理解，減輕心理負擔。
                <br /><br />
                4.
                <strong>時間管理：</strong
                >制定合理的計劃，優先處理事務，保留時間給自己休息。
                <br /><br />
                5.
                <strong>飲食與睡眠：</strong
                >維持均衡飲食，確保充足睡眠，對身心健康有益。
                <br /><br />
                6.
                <strong>創造性活動：</strong
                >嘗試讓自己沈浸在創造性活動中，如繪畫或寫作，轉移注意力，紓解壓力。
                <br /><br />
                7.
                <strong>冥想與放鬆技巧：</strong
                >學習冥想或放鬆技巧，有助於提升心理靈活性，減輕緊張感。
                <br /><br />
                8.
                <strong>尋求專業支持：</strong
                >如果壓力難以自行緩解，考慮尋求心理輔導或醫療支持，專業幫助能提供有效的解決方案。
              </div>
            </div>
            <div
              class="chat-card-item"
              key="7">
              <StressRibbon
                class="stress-ribbon"
                :percent="5" />
              <div class="chat-info">
                1.
                深呼吸：專注深呼吸轉移注意力，紓解壓力。<br />
                2.
                運動：釋放內啡肽，嘗試散步、跑步等活動減輕壓力。<br />
                3.
                交流：與朋友、家人分享感受，獲得支持和建議。<br />
                4.
                時間管理：有效處理壓力，合理安排休息時間。<br />
                5.
                飲食與睡眠：均衡飲食、充足睡眠對減輕壓力有幫助。<br />
                6.
                創造性活動：嘗試繪畫、寫作等活動轉移注意力。<br />
                7.
                專業支持：如壓力難以緩解，建議尋求心理輔導或醫療支持。<br />
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<script setup lang="ts">
import { computed } from '@vue/reactivity';
import DonutChart from '@/components/DonutChart.vue';
import StressRibbon from '@/components/StressRibbon.vue';
import {
  stressPercentColorMap,
  stressPercentLabelMap,
} from '@/utils';

const meanStressLevel = 30 / 50;
const meanStressPercent = computed(() =>
  Math.round(meanStressLevel * 50),
);
const stressColor = computed(() =>
  stressPercentColorMap(meanStressPercent.value),
);
const stressLabel = computed(() =>
  stressPercentLabelMap(meanStressPercent.value),
);
</script>

<style scoped lang="scss">
@import './assets/base.css';

.background {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 100%;
}
.b- {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  width: 100%;
  .scroll-view {
    $BORDER_RADIUS: 0.25em;
    display: flex;
    flex-direction: column;
    position: relative;
    width: 100%;
    .scroll-target {
      position: relative;
      width: 100%;
      height: 100%;
      height: 45vh;
      background-color: var(--color-background-soft);
      border: thin solid var(--color-border);
      border-radius: $BORDER_RADIUS;
      padding: 1em;
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
  .chat-card-list {
    display: flex;
    flex-direction: column;
    position: relative;
    .chat-card-item {
      display: flex;
      flex-direction: row;
      gap: 1em;
      position: relative;
      width: 100%;
      padding: 1em 0.25em;
      .stress-ribbon {
        position: relative;
        width: 0.5em;
        background: linear-gradient(
          to bottom,
          var(--color-border) 0em,
          var(--color-background-mute) 5em,
          var(--color-background-soft) 10em
        );
      }
      .chat-info {
        position: relative;
        width: 100%;
        word-break: break-word;
        white-space: pre-wrap;
      }
    }
  }
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
    .donut-chart {
      position: relative;
      width: 100%;
    }
    .donut-chart-percent {
      display: grid;
      place-items: center;
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      font-size: 2em;
      font-weight: 500;
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
      gap: 2em;
      position: relative;
      width: 100%;
      .a--- {
        $PADDING_BLOCK: 0.25em;
        $PADDING_INLINE: 1em;
        display: flex;
        flex-direction: row;
        align-items: center;
        position: relative;
        border: thin solid var(--color-border);
        border-radius: 1 + 2 * $PADDING_BLOCK;
        > * {
          padding: $PADDING_BLOCK $PADDING_INLINE;
          text-align: center;
        }
        .stress-label {
          $LABEL_MAX_CHARS: 9;
          border-left: thin solid var(--color-border);
          min-width: 2 * $PADDING_INLINE + 0.5em * $LABEL_MAX_CHARS;
          font-weight: bold;
          text-shadow:
            1px 1px 0 var(--color-border),
            1px 0px 0 var(--color-border);
        }
      }
      .b--- {
        position: relative;
        border: thin solid transparent;
        border-radius: 1.5em;
        background-color: var(--color-azure);
        > * {
          padding: 0.25em 1em;
        }
        .upload-file {
          position: relative;
          cursor: pointer;
          color: var(--color-background);
        }
      }
    }
  }
}
</style>
