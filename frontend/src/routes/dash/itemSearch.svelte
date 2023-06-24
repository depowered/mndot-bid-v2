<script>
	import { Search } from 'flowbite-svelte';
	import { Button } from 'flowbite-svelte';
	import { Select } from 'flowbite-svelte';

	let selectedSpecYear = 2022;
	const specYears = [
		{ value: 2022, name: 'Spec Year 2022' },
		{ value: 2020, name: 'Spec Year 2020' },
		{ value: 2018, name: 'Spec Year 2018' }
	];

	let searchValue = '';
	const submitted = () => {
		alert(`Loading results for: ${searchValue}`);
	};
</script>

<form on:submit={submitted} class="flex max-w-4xl m-auto">
	<Select items={specYears} bind:value={selectedSpecYear} class="max-w-min mr-2" />
	<Search
		bind:value={searchValue}
		placeholder="Search by Item Number or Description"
		class="lg:w-[30rem]"
	/>
	<Button type="submit" class="ml-2">Search</Button>
</form>
