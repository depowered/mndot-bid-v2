<script lang="ts">
	import * as Plot from '@observablehq/plot';
	import * as d3 from 'd3';
	import { bids } from '$lib/store';
	import { Tabs, TabItem } from 'flowbite-svelte';

	const renderPlot = (node: HTMLElement, data: Bid[]) => {
		// Filter outliers:
		// Exclude bids with unit prices more than 2 standard deviations above the mean
		const unitPriceArr = data.map((d) => d.unitPrice);
		const unitPriceStd = d3.deviation(unitPriceArr);
		const unitPriceMean = d3.mean(unitPriceArr);
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
				Plot.ruleX([unitPriceMean], { stroke: 'red', strokeWidth: 2 }),
				Plot.textX([unitPriceMean], {
					frameAnchor: 'top-left',
					fill: 'red',
					fontWeight: 'bold',
					text: (d) => `  Mean: ${d.toFixed(2)}`
				})
			]
		};
		node.appendChild(Plot.plot(options));
	};
</script>

{#await $bids then bids}
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
