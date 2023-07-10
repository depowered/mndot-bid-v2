<script lang="ts">
	import { DarkMode, Navbar, NavBrand, NavHamburger, NavUl, NavLi } from 'flowbite-svelte';
	let darkModeBtn =
		'text-gray-500 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-lg p-2.5 fixed right-4 top-32 z-50';
	let navClass = 'bg-ricecake border-gray-200 px-8 py-4 border-b rounded  dark:bg-gray-800';
</script>

<header>
	<Navbar let:hidden let:toggle {navClass}>
		<NavBrand href="/">
			<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
				MnDOT Bid Prices
			</span>
		</NavBrand>
		<NavHamburger on:click={toggle} />
		<NavUl {hidden}>
			<NavLi href="/" active={true} class="text-lg">Home</NavLi>
			<NavLi href="/dash" class="text-lg">Dashboard</NavLi>
			<NavLi><DarkMode size="sm" btnclass={darkModeBtn} /></NavLi>
		</NavUl>
	</Navbar>
</header>
