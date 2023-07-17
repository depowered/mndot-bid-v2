import { initDB } from '$lib/duckdb';

/** @type {import('./$types').PageLoad} */
export function load({ params }) {
  return {
    lazy: {
      // Nested properties will allow the page to render before promises are resolved
      // See: https://kit.svelte.dev/docs/load#streaming-with-promises
      db: initDB()
    }
  };
}
export const ssr = false;