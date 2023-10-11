<script lang="ts">
    import { symptomInputOptionLabels } from "../../lib/symptomInputOptions";
</script>

<link href="/css/input-symptoms.css" rel="stylesheet"/>
<h1>Input Symptoms</h1>
<form>
    {#each symptomInputOptionLabels as symptomInputOptionLabel}
    <div>
        <label>{symptomInputOptionLabel}</label>
        <div>
            <input type="checkbox" />
            <span class="style"/>
        </div>
    </div>
    {/each}
    <button type="submit"></button>
</form>
