<script lang="ts">
	import { Search } from 'flowbite-svelte';
	import { Button } from 'flowbite-svelte';
	import { Select } from 'flowbite-svelte';

	export let searchValue: string;
	export let specYear: number;
	export let submittedSearchValue: string;
	export let submittedSpecYear: number;

	const specYears = [
		{ value: 2020, name: 'Spec Year 2020' },
		{ value: 2018, name: 'Spec Year 2018' },
		{ value: 2016, name: 'Spec Year 2016' }
	];

	const submitted = () => {
		submittedSearchValue = searchValue.toUpperCase();
		submittedSpecYear = specYear;

		// scroll to results
		const el = document.getElementById('item-search');
		if (!el) return;
		el.scrollIntoView({ behavior: 'smooth', block: 'start' });
	};
</script>

<form on:submit|preventDefault={submitted} target="_self" class="flex max-w-4xl mx-auto">
	<Select items={specYears} bind:value={specYear} class="max-w-[170px] mr-2" />
	<Search
		bind:value={searchValue}
		placeholder="Search by Item Number or Description"
		class="lg:w-[30rem]"
	/>
	<Button type="submit" class="ml-2">Search</Button>
</form>
