<script>
	import '../app.postcss';
	import Header from '../lib/components/Header.svelte';
</script>

<Header />
<main class="container mx-auto h-screen">
	<slot />
</main>
