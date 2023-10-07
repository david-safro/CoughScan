<script lang="ts">
    import { symptomInputOptionLabels } from "../../lib/symptomInputOptions";
</script>

<link href="/css/input-symptoms.css"/>
<form>
    {#each symptomInputOptionLabels as symptomInputOptionLabel}
        <label>{symptomInputOptionLabel}</label>
        <input type="text" />
    {/each}
    <button type="submit"></button>
</form>
