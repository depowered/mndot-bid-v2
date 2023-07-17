<script lang="ts">
	import { Span, List, Li, P, AccordionItem, Accordion, Heading } from 'flowbite-svelte';
	import ItemTable from '$lib/components/ItemTable.svelte';
	import ItemSearch from '$lib/components/ItemSearch.svelte';
	import DataVis from '$lib/components/DataVis.svelte';
	import { selectedItemId } from '$lib/store';

	let defaultSearchValue = '';
	let defaultSpecYear = 2020;
	let submittedSearchValue: string;
	let submittedSpecYear: number;

	// import { initDB } from '$lib/duckdb';
	// initDB(); // Start async DuckDB Engine download and db setup
</script>

<section id="#description" class="mx-auto mt-8 max-w-4xl">
	<Accordion>
		<AccordionItem open={true}>
			<span slot="header">About</span>
			<P class="mb-2" weight="semibold" size="xl" color="text-black dark:text-gray-300">
				Gain a better understanding of historic bid item prices on Minnesota Department of
				Transportation (MnDOT) construction projects to help estimate the cost of your next project.
			</P>
			<P class="mb-2" weight="light" color="text-black dark:text-gray-300">
				This tool provides an interface to find price statistics for any item in a construction
				contract since 2018. Insights are powered by data extracted from
				<a
					class="underline hover:no-underline"
					href="https://www.dot.state.mn.us/bidlet/abstract.html"
					target="_blank">Awarded Contract Abstracts</a
				>. The statistics are similar to those already available from MnDOT's annual
				<a
					class="underline hover:no-underline"
					href="https://edocs-public.dot.state.mn.us/edocs_public/DMResultSet/Urlsearch?columns=docnumber,docname,app_id&folderid=28521650"
					target="_blank">Average Bid Price</a
				>
				documents except as follows:
			</P>

			<P class="mb-2 ml-8" weight="light" color="text-black dark:text-gray-300">
				<List tag="ul" class="space-y-1">
					<Li>
						<Span italic>Additional bidders:</Span> Besides bids from the awarded bidder, the abstracts
						include bids from non-awarded bidders and the Engineer's estimate.
					</Li>
					<Li>
						<Span italic>Granularity:</Span> More granular insights, such as price histograms, can be
						derived from the more detailed data.
					</Li>
					<Li>
						<Span italic>Freshness:</Span> New abstracts are ingested shortly after publishing, allowing
						you to gain insights into current-year price trends.
					</Li>
				</List>
			</P>
		</AccordionItem>
		<AccordionItem>
			<span slot="header">Usage</span>
			<P class="mb-2" weight="light" color="text-black dark:text-gray-300">
				Use the search form below to find an item of interest. Items can be searched by their Number
				or Description. The case-insensitive search will accept partial values.
			</P>
			<P class="mb-2" weight="light" color="text-black dark:text-gray-300">
				<P class="mb-2" weight="light" color="text-black dark:text-gray-300">Search Examples</P>
				<List tag="ul" class="space-y-1 ml-8">
					<Li>2575 -> All turf establishment items</Li>
					<Li>common -> EXCAVATION - COMMON and similar</Li>
					<Li>24" rc pipe sewer -> 24 inch reinforced concrete storm sewer items</Li>
				</List>
			</P>
			<P class="mb-2" weight="light" color="text-black dark:text-gray-300">
				Items with bid records to view will have an orange button in the leftmost column. Click the
				button to view summary statistics for that item. Items with a greater contract occurrence
				will provide more useful statistics.
			</P>
		</AccordionItem>
		<AccordionItem>
			<span slot="header">Disclaimer</span>
			<P class="mb-2" weight="medium" color="text-black dark:text-gray-300">
				The data provided by this application is for informational purposes only and is provided
				"as-is" without any warranty, express or implied. The data may not be complete, accurate, or
				up-to-date, and may be subject to change without notice. The data should not be used as the
				sole basis for any decision making.
			</P>
		</AccordionItem>
	</Accordion>
</section>

<section id="item-search" class="mt-16 max-w-4xl mx-auto">
	<div class="flex flex-col text-center">
		<Heading tag="h2" customSize="text-3xl" class="mb-4">Item Search</Heading>
		<ItemSearch
			searchValue={defaultSearchValue}
			specYear={defaultSpecYear}
			bind:submittedSearchValue
			bind:submittedSpecYear
		/>
		{#if submittedSearchValue}
			<ItemTable bind:submittedSearchValue bind:submittedSpecYear />
		{/if}
	</div>
</section>

<section id="view-bids" class="mt-16 mb-24 max-w-4xl mx-auto h-[600px]">
	<div class="flex flex-col text-center">
		{#if $selectedItemId}
			<Heading tag="h2" customSize="text-3xl" class="mb-4">Bid Data Summary</Heading>
			<DataVis />
		{/if}
	</div>
</section>
