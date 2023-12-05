import { percentColorMap_RYG } from '@/utils';
import { defineStore } from 'pinia';
import { fetchUtil } from '@/utils';

const defaultState = () => ({
  _category: undefined as EmoCategoryList | undefined,
  _highPercent: 0,
  _length: undefined as number | undefined,
  _level: 0,
  _smoothLevel: 0,
  _tick: undefined as number | undefined,
});

export const useEmoLevelStore = defineStore('emoLevel', {
  state: defaultState,
  getters: {
    category: (state) => state._category ?? 'emotion',
    categoryCapped(): string {
      return (
        this.category.charAt(0).toUpperCase() +
        this.category.slice(1)
      );
    },
    color(): string {
      if (this._tick === undefined) {
        return 'var(--color-border)';
      }
      return percentColorMap_RYG(this.percent);
    },
    label(): string {
      if (
        this._tick === undefined ||
        this._category === undefined
      ) {
        return 'Unknown';
      }
      for (const [label, threshold] of Object.entries(
        EmoLabelThresholdMap[this._category],
      )) {
        if (this.percent >= threshold) {
          return label;
        }
      }
      return 'Unknown';
    },
    length: (state) => state._length,

    // predicted level
    level: (state) => state._level,

    // high level percentage by moving window mean
    highPercent: (state) => state._highPercent,

    // smoothed level in percentage
    percent(): number {
      return (
        this._smoothLevel *
        EmoLevelPercentFactorMap[this.category]
      );
    },

    // rounded smoothed level in percentage
    percentRounded(): number {
      return Math.round(this.percent);
    },

    // smoothed level by moving window mean
    smoothLevel: (state) => state._smoothLevel,

    // starts from 1
    tick: (state) => state._tick,
  },
  actions: {
    $reset() {
      // tick should be the first to reset
      this._tick = undefined;

      this.$patch(defaultState());
    },
    async getLevels(file: File) {
      this.$reset();

      // parse file
      const body = await file.text();
      const { category } = JSON.parse(body);
      if (!EmoCategoryList.includes(category)) {
        throw new Error(
          'The emotion level file has no valid category',
        );
      }

      // fetch API
      const response = await fetchUtil(
        `/${category}/levels`,
        body,
      );
      if (!response.ok) {
        throw new Error(
          `${response.status} ${response.statusText}`,
        );
      }

      this._category = category;

      // read header
      const streamLengthHeader = response.headers.get(
        'X-Stream-Length',
      );
      if (streamLengthHeader !== null) {
        this._length = parseInt(streamLengthHeader);
      }

      // stream reader and decoder
      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('The response has no body');
      }
      const decoder = new TextDecoder('utf-8');

      // moving window
      const movingWindow: number[] = [];
      const movingWindowCap = 100;
      const highLevelThreshold =
        80 / EmoLevelPercentFactorMap[this.category];
      const isHighLevel = (level: number) =>
        level >= highLevelThreshold;

      // read stream
      for (let done = false, tick = 1; !done; tick += 1) {
        const chunk = await reader.read();
        if (chunk.done) {
          done = true;
        } else {
          this._level = parseFloat(decoder.decode(chunk.value));

          // move the window
          movingWindow.push(this._level);
          if (movingWindow.length > movingWindowCap) {
            movingWindow.shift();
          }

          // calculate the mean value in window
          this._smoothLevel =
            movingWindow.reduce((acc, curr) => acc + curr, 0) /
            movingWindow.length;

          // calculate the high level percentage in window
          this._highPercent =
            (movingWindow.filter(isHighLevel).length /
              movingWindow.length) *
            100;

          // add tick
          this._tick = tick;
        }
      }
    },
  },
});

const EmoCategoryList = ['stress'] as const;

type EmoCategoryList = (typeof EmoCategoryList)[number];

const EmoLabelThresholdMap = {
  emotion: {},
  stress: {
    Stressful: 75,
    Tense: 50,
    Neutral: 25,
    Relaxed: 0,
  } as const,
} as const;

const EmoLevelPercentFactorMap = {
  emotion: 1,
  stress: 50,
} as const;
