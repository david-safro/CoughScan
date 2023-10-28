import adapter from '@sveltejs/adapter-node';
import preprocess from 'svelte-preprocess';

export default {
  kit: {
    adapter: adapter(),
  },
  preprocess: preprocess({
    typescript: true,
  }),
};
