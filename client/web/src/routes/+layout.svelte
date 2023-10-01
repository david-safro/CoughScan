<script lang="ts">
    import { onMount } from "svelte";
    import Device from "svelte-device-info";
    import Footer from "../components/footer.svelte";
    import Navbar from "../components/navbar.svelte";

    onMount(() => {
        const fadeContainer = document.getElementById("fade-container") as HTMLDivElement;
        const resizeHandler = () => {
            fadeContainer.style.opacity = "1";
            document.documentElement.style.fontSize = `${window.innerWidth / (325 / 2)}px`;
        };
        resizeHandler();
        window.addEventListener('resize', resizeHandler);

        if (Device.isMobile) {
            alert("This website was not designed for mobile. Download the app for a better experience");
        }
        return () => {
            window.removeEventListener('resize', resizeHandler);
        };
    });
</script>

<Navbar />
<div id="fade-container">
    <main>
        <slot />
    </main>
</div>
<Footer />
