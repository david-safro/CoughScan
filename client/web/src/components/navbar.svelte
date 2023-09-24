<script lang="ts">
    const navItems = [
        { title: "Cough Test", href: "/cough-test" },
        { title: "Input Symptoms", href: "/input-symptoms" },
        { title: "About", href: "/about" }
    ];
</script>

<link rel="stylesheet" href="/css/navbar.css"/>
<nav id="navbar">
    <a href="/">
        <h1><img src="/img/logo.svg"/>Cough<span>Scan</span></h1>
    </a>
    <ul>
        {#each navItems as { title, href }}
            <li>
                <a href={href}>
                    {title}
                </a>
            </li>
        {/each}
    </ul>
</nav>

