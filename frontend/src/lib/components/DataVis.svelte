<script>
	import { Tabs, TabItem } from 'flowbite-svelte';
	import AvgPriceTable from './AvgPriceTable.svelte';
</script>

<div class="mt-8 mb-24">
	<Tabs style="underline">
		<TabItem open title="Weighted Average">
			<AvgPriceTable />
		</TabItem>
		<TabItem title="Price vs Quantity">
			<p class="text-sm text-gray-500 dark:text-gray-400">
				<b>Dashboard:</b> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
				incididunt ut labore et dolore magna aliqua.
			</p>
		</TabItem>
	</Tabs>
</div>
