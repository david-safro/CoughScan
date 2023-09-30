<script lang="ts">
    import { onMount } from "svelte";
    import Footer from "../components/footer.svelte";
    import Navbar from "../components/navbar.svelte";

    onMount(() => {
        (document.getElementById("fade-container") as HTMLDivElement).style.opacity = "1";
        onresize = () => {
            document.documentElement.style.fontSize = `${window.innerWidth / (325/2)}px`;
        }
    });

</script>
<Navbar />
<div id="fade-container">
    <main>
        <slot />
    </main>
</div>
<Footer />