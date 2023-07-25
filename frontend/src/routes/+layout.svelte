<script>
	import '../app.postcss';
	import Header from '../lib/components/Header.svelte';
	import SiteFooter from '../lib/components/SiteFooter.svelte';
</script>

<Header />
<main class="container mx-auto">
	<slot />
</main>

<SiteFooter />
