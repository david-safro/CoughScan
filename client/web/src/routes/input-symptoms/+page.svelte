<script lang="ts">
    import { symptomInputOptionLabels } from "../../lib/symptomInputOptions";
    import type { PageData } from "./$types";

    export function handleCheck(e: Event) {
        (document.getElementsByClassName((e.target as HTMLInputElement).dataset["name"]!)[0] as HTMLInputElement).value = (e.target as HTMLInputElement).checked.toString()
    }

    async function handleSubmit(event: SubmitEvent) {
        event.preventDefault();

        const formData = new FormData(event.target as HTMLFormElement);
        const formDataObject:any = {};
        formData.forEach((value, key) => {
            formDataObject[key] = value;
        });

        try {
            const response = await fetch('http://127.0.0.1:5000/predict_symptoms', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                body: JSON.stringify(formDataObject)
            });

            if (response.ok) {
                const responseData = await response.json();
                console.log('Response from server:', responseData);
                let symptomInputOptions: any = {};
                formData.forEach((value, key) => {
                    symptomInputOptions[key] = value;
                });
                const pageData: PageData = {
                    diagnosisInfo: responseData,
                    symptomInputOptions
                };
                window.location.href = `/diagnosis/${encodeURIComponent(JSON.stringify(responseData))}`

            } else {
                console.error('Server returned an error:', response.status);
            }
        } catch (error) {
            console.error('Error while sending the data', error);
        }



        //temp

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
            <input type="checkbox" data-name={propertyName} on:change={handleCheck}/>
            <input type="hidden" name={propertyName} class={propertyName} value="false"/>
            {/if}
            <span class="style"/>
        </div>
    </div>
    {/each}
    <button type="submit">Submit</button>
</form>
