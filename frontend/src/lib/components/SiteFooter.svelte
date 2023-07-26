<script>
	import { Footer, FooterCopyright, FooterLinkGroup, FooterLink } from 'flowbite-svelte';
</script>

<Footer class="bg-gray-100 dark:bg-gray-800">
	<FooterCopyright
		href="https://www.linkedin.com/in/devin-power/"
		by="Devin Power"
		year={2023}
		copyrightMessage=""
	/>
	<FooterLinkGroup
		ulClass="flex flex-wrap items-center mt-3 text-sm text-gray-500 dark:text-gray-400 sm:mt-0"
	>
		<FooterLink href="https://github.com/depowered/mndot-bid-v2">GitHub</FooterLink>
		<FooterLink href="https://github.com/depowered/mndot-bid-v2/blob/main/LICENSE"
			>License</FooterLink
		>
	</FooterLinkGroup>
</Footer>
