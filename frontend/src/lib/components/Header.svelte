<script lang="ts">
	import { DarkMode, Navbar, NavBrand, NavHamburger, NavUl, NavLi } from 'flowbite-svelte';
</script>

<header>
	<Navbar let:hidden let:toggle class="bg-gray-100 dark:bg-gray-800 rounded-none">
		<NavBrand href="/">
			<span class="self-center whitespace-nowrap text-2xl font-semibold dark:text-white">
				MnDOT Bid Prices
			</span>
		</NavBrand>
		<NavHamburger on:click={toggle} />
		<NavUl {hidden}>
			<NavLi><DarkMode size="md" /></NavLi>
		</NavUl>
	</Navbar>
</header>
