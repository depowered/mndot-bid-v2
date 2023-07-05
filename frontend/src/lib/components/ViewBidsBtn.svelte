<script lang="ts">
	import { Button } from 'flowbite-svelte';

	export let disabled = false;
</script>

<Button {disabled} class="w-8 h-8 p-0">
	{#if disabled}
		<img src="/xmark-solid.svg" alt="x icon" class="h-5 w-5" />
	{:else}
		<img src="/chart-icon.svg" alt="chart icon" class="h-5 w-5" />
	{/if}
</Button>
