import { percentColorMap_RYG } from '@/utils';
import { defineStore } from 'pinia';
import { fetchUtil } from '@/utils';

export const useEmoLevelStore = defineStore('emoLevel', {
  state: () => ({
    _category: undefined as 'stress' | undefined,
    _length: undefined as number | undefined,
    _level: 0,
    _smoothLevel: 0,
    _tick: undefined as number | undefined,
  }),
  getters: {
    category(): 'stress' | 'emotion' {
      if (
        this._tick === undefined ||
        this._category === undefined
      ) {
        return 'emotion';
      }
      return this._category;
    },
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
    label() {
      if (
        this._tick === undefined ||
        this._category === undefined
      ) {
        return 'Unknown';
      }
      if (this.percent < 25) return 'Relaxed';
      if (this.percent < 50) return 'Neutral';
      if (this.percent < 75) return 'Tense';
      return 'Stressful';
    },
    length: (state) => state._length,
    level: (state) => state._level,

    // already smoothed
    percent: (state) => state._smoothLevel * 50,
    percentRounded(): number {
      return Math.round(this.percent);
    },
    smoothLevel: (state) => state._smoothLevel,

    // starts from 1
    tick: (state) => state._tick,
  },
  actions: {
    $reset() {
      // tick should be the first to reset
      this._tick = undefined;

      this._category = undefined;
      this._length = undefined;
      this._level = 0;
      this._smoothLevel = 0;
    },
    async getLevels(file: File) {
      this.$reset();

      // parse file
      const body = await file.text();
      const { category } = JSON.parse(body);
      if (category === undefined) {
        throw new Error('The emolevel file has no category');
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
      const movingWindowCap = 60;

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

          // add tick
          this._tick = tick;
        }
      }
    },
  },
});
