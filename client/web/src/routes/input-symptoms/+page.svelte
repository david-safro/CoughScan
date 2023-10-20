<script lang="ts">
    import { redirect } from "@sveltejs/kit";
    import { symptomInputOptionLabels } from "../../lib/symptomInputOptions";
    import type { PageData } from "./$types";

    async function handleSubmit(event: SubmitEvent) {
        event.preventDefault();

        const formData = (event.target as HTMLFormElement).formData;

        /*
        try {
            const response = await fetch('/your-server-endpoint', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const responseData = await response.json();
                console.log('Response from server:', responseData);
            } else {
                console.error('Server returned an error:', response.status);
            }
        } catch (error) {
            console.error('Error while sending the data', error);
        }
        */

        //temp
        const responseData: PageData = {
            diagnosisInfo: {
                certainty: 84.7,
                diagnosis: true
            },
            coughTestOptions: {
                age: 14,
                gender: "male",
                respiratoryCondition: "yes",
                feverMusclePain: false,
                healthStatus: "healthy"
            }
        };
        throw redirect(303, `/diagnosis/${encodeURIComponent(JSON.stringify(responseData))}`)
    }
</script>

<link href="/css/input-symptoms.css" rel="stylesheet"/>
<h1>Input Symptoms</h1>
<form action="/" method="post" on:submit={handleSubmit}>
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
