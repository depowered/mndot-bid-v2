<script lang="ts">
	import * as Plot from '@observablehq/plot';
	import * as d3 from 'd3';
	import { bids } from '$lib/store';
	import { Tabs, TabItem, P } from 'flowbite-svelte';

	const renderPlot = (node: HTMLElement, data: Bid[]) => {
		// Filter outliers:
		// Exclude bids with unit prices more than 2 standard deviations above the mean
		const unitPriceArr = data.map((d) => d.unitPrice);
		const unitPriceStd = d3.deviation(unitPriceArr);
		const unitPriceMean = d3.mean(unitPriceArr);
		const unitPriceMedian = d3.median(unitPriceArr);
		const upperBounds = unitPriceMean + 2 * unitPriceStd;
		const filtered = data.filter((d) => d.unitPrice <= upperBounds);

		const options = {
			className: 'plot',
			marginTop: 40,
			marginRight: 40,
			marginBottom: 40,
			marginLeft: 40,
			grid: true,
			inset: 10,
			x: {
				label: 'Unit Price ($)'
			},
			y: {
				label: 'Frequency'
			},
			marks: [
				Plot.rectY(
					filtered,
					Plot.binX(
						{ y: 'count' },
						{
							x: 'unitPrice',
							fill: '#4e79a7',
							thresholds: 'freedman-diaconis',
							tip: 'x'
						}
					)
				),
				Plot.ruleX([unitPriceMedian], { stroke: 'red', strokeWidth: 2 }),
				Plot.textX([unitPriceMedian], {
					frameAnchor: 'top-left',
					fill: 'red',
					fontWeight: 'bold',
					text: (d) => `  Median: $${d.toFixed(2)}`
				})
			]
		};
		node.appendChild(Plot.plot(options));
	};
</script>

{#await $bids then bids}
	<p class="dark:text-white text-xl text-center">Unit Price Histograms</p>
	<P class="mt-2" weight="light" color="text-black dark:text-gray-300">
		The histogram figures below provide a graphical representation of the distribution of unit
		prices within the dataset. Prior to figure generation, outliers greater than two standard
		deviations above the mean are excluded. This helps focus the figure on more relevant price
		groupings. The median, rather than the mean, is shown for similar reasons.
	</P>
	<P class="mt-2" weight="light" color="text-black dark:text-gray-300">
		Note that the figure for each category is generated separately, so the auto-binning algorithm
		may result in bins of different sizes. Hover over the figure to show a tooltip with additional
		details about each bin.
	</P>
	<div class="flex flex-col items-center">
		<Tabs style="underline">
			<TabItem open title="Winning Bids">
				<div
					id="winning-bid-hist"
					use:renderPlot={bids.filter((d) => d.category === 'winning')}
					class="mt-4 mb-8"
				/>
			</TabItem>
			<TabItem title="Losing Bids" class="items-center">
				<div
					id="losing-bid-hist"
					use:renderPlot={bids.filter((d) => d.category === 'losing')}
					class="mt-4 mb-8"
				/>
			</TabItem>
			<TabItem title="Engineer's Estimate">
				<div
					id="engineers-est-hist"
					use:renderPlot={bids.filter((d) => d.category === 'engineers')}
					class="mt-4 mb-8"
				/>
			</TabItem>
		</Tabs>
	</div>
{/await}

<style>
</style>
