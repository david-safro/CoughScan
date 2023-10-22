<script lang="ts">
    import { onDestroy, onMount, setContext, tick } from "svelte";
    import Device from "svelte-device-info";
    import Footer from "../components/footer.svelte";
    import Navbar from "../components/navbar.svelte";

    let fadeContainer: HTMLDivElement

    function triggerAnimation() {
        fadeContainer = document.getElementById("fade-container") as HTMLDivElement;
        fadeContainer.style.opacity = "1";
    }

    onMount(() => {
        triggerAnimation()
        const resizeHandler = () => {
            document.documentElement.style.fontSize = `${window.innerWidth / (325 / 2)}px`;
        };
        resizeHandler();
        window.addEventListener('resize', resizeHandler);

        if (Device.isMobile) {
            alert("This website was not designed for mobile. Download the app for a better experience");
        }
        return () => {
            fadeContainer.style.opacity = "0";
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
