<template>
  <header></header>

  <main>
    <div class="background">
      <section class="u-">
        <section class="a--">
          <DonutChart
            class="ring"
            :percent="meanStressLevelPercent"
            :foreground-color="stressLevelColor"
            background-color="var(--color-background-mute)"
            :stroke-width-percent="15" />
          <div class="ring-percent">
            {{ meanStressLevelPercent }}%
          </div>
        </section>
        <section class="b--">
          <div class="cabinet">
            <section class="a---">
              <div class="">Stress Level</div>
              <div class="split"></div>
              <div class="stress-level-str" :style="{
                color: stressLevelColor,
                fontWeight: 'bold',
              }">{{ stressLevelString }}</div>
            </section>
            <section class="b---">
              <div class="upload-file">Upload</div>
            </section>
          </div>
        </section>
      </section>
      <section class="b-">
        <div class="scroll-view">
          <div class="scroll-target">
            <section class="a--">

            </section>
            <section class="b--">

            </section>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<script setup lang="ts">
import { computed } from '@vue/reactivity';
import DonutChart from './components/DonutChart.vue';
import { percentColorMap_G2R } from './utils';

const meanStressLevel = 100 / 50;
const meanStressLevelPercent = computed(() =>
  Math.round(meanStressLevel * 50),
);
const stressLevelColor = computed(() =>
  percentColorMap_G2R(meanStressLevelPercent.value),
);
const stressLevelString = computed(() => {
  const percent = meanStressLevelPercent.value;
  if (percent > 80) return 'Very Stressful';
  if (percent > 60) return 'Stressful';
  if (percent > 20) return 'Neutral';
  return 'Relaxed';
});
</script>

<style scoped lang="scss">
@import './assets/base.css';

.background {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  padding: 5%;
}
.b- {
  display: flex;
  flex-direction: row;
  position: relative;
  border: thin solid var(--color-border);
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
    .ring {
      position: relative;
      width: 100%;
    }
    .ring-percent {
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
      height: 100%;
      .a--- {
        display: flex;
        flex-direction: row;
        align-items: center;
        position: relative;
        height: 100%;
        border: thin solid var(--color-border);
        border-radius: 1.5em;
        > * {
          padding: 0.25em 1em;
        }
        .split {
          position: relative;
          border-left: thin solid var(--color-border);
          padding: 0;
          height: 85%;
        }
        .stress-level-str {
          text-shadow: 0.1em 0.1em var(--color-background-mute);
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
          color: var(--color-background);
          font-weight: bold;
        }
      }
    }
  }
}
/* header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
} */

/* @media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(
      var(--section-gap) / 2
    );
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
} */
</style>
