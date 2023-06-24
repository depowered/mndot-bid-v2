<script>
	import '../app.postcss';
	import Header from './Header.svelte';
</script>

<Header />
<main class="container mx-auto p-16 h-screen">
	<slot />
</main>
