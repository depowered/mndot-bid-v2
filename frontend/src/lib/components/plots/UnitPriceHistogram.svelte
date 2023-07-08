<script lang="ts">
	import * as Plot from '@observablehq/plot';
	import { bids } from '$lib/store';
	import { Tabs, TabItem } from 'flowbite-svelte';

	const renderPlot = (node: HTMLElement, data: Bid[]) => {
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
			marks: [
				Plot.rectY(
					data,
					Plot.binX(
						{ y: 'count' },
						{
							x: 'unitPrice',
							fill: '#4e79a7',
							thresholds: 'freedman-diaconis',
							tip: 'x'
						}
					)
				)
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
