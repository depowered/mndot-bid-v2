<script>
	import { initDB } from '$lib/duckdb';
	import '../app.postcss';
	import Header from '../lib/components/Header.svelte';

	// Initialize the db and load data from remote parquets in an web worker
	// Called here to get the async process started as soon as the page loads
	initDB();
</script>

<Header />
<main class="container mx-auto h-screen">
	<slot />
</main>
