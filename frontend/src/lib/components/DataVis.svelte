<script>
	import { Tabs, TabItem } from 'flowbite-svelte';
	import AvgPriceTable from './AvgPriceTable.svelte';
	import UnitPriceHistogram from './plots/UnitPriceHistogram.svelte';
</script>

<div class="mt-8 mb-24">
	<Tabs style="underline">
		<TabItem open title="Weighted Average">
			<AvgPriceTable />
		</TabItem>
		<TabItem title="Unit Price Histogram">
			<UnitPriceHistogram />
		</TabItem>
	</Tabs>
</div>
