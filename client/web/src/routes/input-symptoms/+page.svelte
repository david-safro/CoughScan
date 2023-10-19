<script lang="ts">
    import { symptomInputOptionLabels } from "../../lib/symptomInputOptions";
</script>

<link href="/css/input-symptoms.css" rel="stylesheet"/>
<h1>Input Symptoms</h1>
<form action="/" method="post">
    {#each symptomInputOptionLabels as [symptomInputOptionLabel, propertyName]}
    <div>
        <label for={propertyName}>{symptomInputOptionLabel}</label>
        <div>
            {#if symptomInputOptionLabel.includes("[")}
            <select name={propertyName}>
                {#each symptomInputOptionLabel.substring(
                    symptomInputOptionLabel.indexOf("[") + 1,
                    symptomInputOptionLabel.indexOf("]")
                ).split(", ") as option}
                    <option value={option.replace(" ", "-").toLowerCase()}>{option}</option>
                {/each}
            </select>
            {:else}
            <input type="checkbox" name={propertyName} value="true" on:change={e => e.target.value = e.target.checked}/>
            <input type="hidden" name={propertyName} value="false"/>
            {/if}
            <span class="style"/>
        </div>
    </div>
    {/each}
    <button type="submit">Submit</button>
</form>
