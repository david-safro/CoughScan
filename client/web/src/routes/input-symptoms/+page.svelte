<script lang="ts">
    import { symptomInputOptionLabels } from "../../lib/symptomInputOptions";
    import type { PageData } from "./$types";

    async function handleSubmit(event: SubmitEvent) {
        event.preventDefault();

        const formData = new FormData(event.target as HTMLFormElement);

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

        let symptomInputOptions: any = {};
        formData.forEach((value, key) => {
            symptomInputOptions[key] = value;
        });

        //temp
        const responseData: PageData = {
            diagnosisInfo: {
                certainty: 84.7,
                diagnosis: true,
                type: "symptoms"
            },
            symptomInputOptions
        };
        window.location.href = `/diagnosis/${encodeURIComponent(JSON.stringify(responseData))}`
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
            <input type="checkbox" name={propertyName} value="true"/>
            <input type="hidden" name={propertyName} value="false"/>
            {/if}
            <span class="style"/>
        </div>
    </div>
    {/each}
    <button type="submit">Submit</button>
</form>
