import { defineStore } from 'pinia';
import { fetchUtil } from '@/utils';

export const useMonoConsultStore = defineStore(
  'monoConsultStore',
  {
    state: () => ({
      _percent: 0,
      _text: '',
    }),
    getters: {
      percent: (state) => state._percent,
      text: (state) => state._text,
    },
    actions: {
      $reset() {
        this._percent = 0;
        this._text = '';
      },
      async get({
        category,
        percent,
      }: {
        category: 'stress';
        percent: number;
      }) {
        this.$reset();

        // fetch API
        const response = await fetchUtil(
          `/${category}/consult/mono`,
          JSON.stringify({
            percent,
          }),
        );
        if (!response.ok) {
          throw new Error(
            `${response.status} ${response.statusText}`,
          );
        }

        this._percent = percent;

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
            this._text += decoder.decode(chunk.value);
            console.log(this.text);
          }
        }
      },
    },
  },
);
