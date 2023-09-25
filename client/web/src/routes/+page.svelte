<script lang="ts">
    export function navigateToInputSymptoms() {
        window.location.href = "/input-symptoms";
    }
    export function navigateToCoughTest() {
        window.location.href = "/cough-test";
    }
</script>

<link rel="stylesheet" href="/css/home.css"/>
<div>
    <h1>
        Do I have Covid?
     </h1>
    <p>
        Try two tests to get an estimate
    </p>
    <div>
        <button on:click={navigateToCoughTest}>
            Cough Test
        </button>
        <button on:click={navigateToInputSymptoms}>
            Input Symptoms
        </button>
    </div>
</div>
<img />
