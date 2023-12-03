import { stressPercentColorMap } from '@/utils';
import { defineStore } from 'pinia';

export const useStressLevelStore = defineStore('stressLevel', {
  state: () => ({
    mean: 0,
  }),
  getters: {
    level: (state) => state.mean,
    percent: (state) => state.mean * 50,
    percentRounded(): number {
      return Math.round(this.percent);
    },
    color(): string {
      return stressPercentColorMap(this.percent);
    },
    label(): string {
      if (this.percent < 25) return 'Relaxed';
      if (this.percent < 50) return 'Neutral';
      if (this.percent < 75) return 'Tense';
      return 'Stressful';
    },
  },
  actions: {
    $reset() {
      this.mean = 0;
    },
  },
});
