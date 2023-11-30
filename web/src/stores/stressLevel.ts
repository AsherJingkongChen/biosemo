import {
  stressPercentColorMap,
  stressPercentLabelMap,
} from '@/utils';
import { defineStore } from 'pinia';

export const useStressLevelStore = defineStore(
  'stressLevel',
  {
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
        return stressPercentLabelMap(this.percent);
      },
    },
  },
);
