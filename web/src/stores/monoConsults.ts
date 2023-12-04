import { defineStore } from 'pinia';
import { fetchUtil } from '@/utils';

const defaultState = () => ({
  _items: [
    {
      percent: 0,
      text:
        'Welcome! ' +
        'Share your feelings with us. ' +
        "Let's start this journey together!",
    },
    {
      percent: 0,
      text:
        'Welcome! ' +
        'Share your feelings with us. ' +
        "Let's start this journey together!",
    },
    {
      percent: 0,
      text:
        'Welcome! ' +
        'Share your feelings with us. ' +
        "Let's start this journey together!",
    },
    {
      percent: 0,
      text:
        'Welcome! ' +
        'Share your feelings with us. ' +
        "Let's start this journey together!",
    },
    {
      percent: 0,
      text:
        'Welcome! ' +
        'Share your feelings with us. ' +
        "Let's start this journey together!",
    },
  ],
  _running: false,
});

export const useMonoConsultsStore = defineStore(
  'monoConsultsStore',
  {
    state: defaultState,
    getters: {
      length: (state) => state._items.length,
      running: (state) => state._running,
    },
    actions: {
      $reset() {
        this.$patch(defaultState());
      },
      async push({
        category,
        percent,
      }: {
        category: string;
        percent: number;
      }) {
        this._running = true;

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

        // stream reader and decoder
        const reader = response.body?.getReader();
        if (!reader) {
          throw new Error('The response has no body');
        }
        const decoder = new TextDecoder('utf-8');

        // register a new item
        const item = {
          percent,
          text: '',
        };
        this._items.push(item);

        // read stream
        for (let done = false; !done; ) {
          const chunk = await reader.read();
          if (chunk.done) {
            done = true;
          } else {
            item.text += decoder.decode(chunk.value);
          }
        }

        // done
        this._running = false;
      },
      [Symbol.iterator]() {
        return this._items.values();
      },
    },
  },
);
