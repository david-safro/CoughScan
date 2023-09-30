<script lang="ts">
    import { onMount } from "svelte";
    import Device from "svelte-device-info"
    import Footer from "../components/footer.svelte";
    import Navbar from "../components/navbar.svelte";

    onMount(() => {
        (document.getElementById("fade-container") as HTMLDivElement).style.opacity = "1";
        onresize = () => {
            document.documentElement.style.fontSize = `${window.innerWidth / (325/2)}px`;
        }

        if (Device.isMobile) alert("This website was not designed for mobile. Download the app for a better experience");
    });

</script>

<Navbar />
<div id="fade-container">
    <main>
        <slot />
    </main>
</div>
<Footer />