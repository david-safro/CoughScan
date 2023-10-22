<script lang="ts">
    const navItems = [
        { title: "Guide", href: "/guide" },
        { title: "Cough Test", href: "/cough-test" },
        { title: "Input Symptoms", href: "/input-symptoms" }
    ];
</script>

<link rel="stylesheet" href="/css/navbar.css"/>
<nav id="navbar">
    <a on:click={() => {window.location.href = "/"}}>
        <h1><img src="/img/logo.svg"/>Cough<span>Scan</span></h1>
    </a>
    <ul>
        {#each navItems as { title, href }}
            <li>
                <a on:click={() => {window.location.href = href}}>
                    {title}
                </a>
            </li>
        {/each}
    </ul>
</nav>

