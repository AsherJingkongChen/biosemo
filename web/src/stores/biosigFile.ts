import { defineStore } from 'pinia';
import { fetchUtil } from '@/utils';

export const useBiosigFileStore = defineStore('biosigFile', {
  state: () => ({
    _category: undefined as 'stress' | undefined,
    _length: undefined as number | undefined,
    _level: 0,
    _tick: 0,
  }),
  getters: {
    category: (state) => state._category,
    length: (state) => state._length,
    level: (state) => state._level,
    tick: (state) => state._tick,
  },
  actions: {
    $reset() {
      this._category = undefined;
      this._length = undefined;
      this._level = 0;

      // tick should be the last to reset
      this._tick = 0;
    },
    async getLevels(file: File): Promise<void> {
      this.$reset();

      // parse file
      const body = await file.text();
      const { category } = JSON.parse(body);
      this._category = category;

      // fetch API
      const response = await fetchUtil(
        `/biosig/levels/${category}`,
        body,
      );
      if (!response.ok) {
        throw new Error(
          `${response.status} ${response.statusText}`,
        );
      }

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

      // read stream
      for (let done = false; !done; ) {
        const chunk = await reader.read();
        if (chunk.done) {
          done = true;
        } else {
          this._level = parseFloat(decoder.decode(chunk.value));
          this._tick += 1;
        }
      }
    },
  },
});
