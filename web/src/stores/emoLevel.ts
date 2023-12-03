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
    category: (state) => state._category,
    color(): string {
      if (this._tick === undefined) {
        return 'var(--color-border-hover)';
      }
      return percentColorMap_RYG(this.percent);
    },
    label() {
      if (this._category === 'stress') {
        if (this.percent < 25) return 'Relaxed';
        if (this.percent < 50) return 'Neutral';
        if (this.percent < 75) return 'Tense';
        return 'Stressful';
      }
      return;
    },
    length: (state) => state._length,
    level: (state) => state._level,
    smoothLevel: (state) => state._smoothLevel,
    percent: (state) => state._smoothLevel * 50,
    percentRounded(): number {
      return Math.round(this.percent);
    },
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
      let movingWindow: number[] = [];
      const movingWindowCap = 60;

      // read stream
      this._tick = 0;
      for (let done = false; !done; ) {
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
          this._tick += 1;
        }
      }
    },
  },
});
