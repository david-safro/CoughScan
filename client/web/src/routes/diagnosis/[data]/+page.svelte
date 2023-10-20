<script lang="ts">
  import { onMount } from "svelte";
  import { coughTestOptionLabels } from "$lib/coughTestOptions";
  import { symptomInputOptionLabels } from "$lib/symptomInputOptions";
  import type { PageData } from "./$types";
  import { spread } from "axios";

    export let data: PageData
    let diagnosisInfo: DiagnosisInfo = data.diagnosisInfo;

    let options: CoughTestOptions | SymptomInputOptions = diagnosisInfo.type == "cough" ? data.coughTestOptions : data.symptomInputOptions;
    let info: Array<Array<any>> = []
    let labels = diagnosisInfo.type == "cough" ? coughTestOptionLabels : symptomInputOptionLabels;

    function populateUserOptions() {
        let i = 0;
        for (const value of Object.values(options)) {
            if (i > labels.length) return;
            info[i] = [labels[i][0], value];
            i++;
        }
    }

    populateUserOptions();

    onMount(() =>  {
        setTimeout(() => {
            setCertaintyDisplay(diagnosisInfo.certainty);
        }, 200)
    })

    function setCertaintyDisplay(percent: number) {
        const certaintyDisplayStyle: CSSStyleDeclaration = (document.getElementById("certainty-display") as HTMLDivElement).style;

        let i = 0;
        const interval = setInterval(() => {
            i += 2;
            certaintyDisplayStyle.backgroundImage = `conic-gradient(var(--secondary) ${i * 3.6}deg, #fff 0deg)`; // i/100 * 3.6 = 3.6i/360deg

            if (i >= percent) clearInterval(interval);
        }, 1);
    }

    export function saveDiagnosis() {
        alert("Link copied to clipboard!")
        navigator.clipboard.writeText(window.location.href)
    }
</script>

<link rel="stylesheet" href="/css/diagnosis.css"/>

<div id="container">
    <button class="save" on:click={saveDiagnosis}>
        Save Diagnosis
    </button>
    <div class="upper">
        <h1>Prediction: <span class={diagnosisInfo.diagnosis.toString()}>{diagnosisInfo.diagnosis ? "Positive" : "Negative"}</span></h1>
    </div>
    <div class="lower">
        <div id="certainty-display">
            <div id="certainty-text">
                <h2><span>{diagnosisInfo.certainty}%</span> Certainty</h2>
                <p>You can retake the test more times for increased accuracy.</p>
            </div>
        </div>
        <div id="right">
            <ul id="user-options">
                {#each info as option}
                    <li>
                        <span><b>{option[0]}: </b>{option[1]}</span>
                    </li>
                {/each}
            </ul>
            <div id="info">
                <p>
                    Ensure the information entered above is accurate. If it isn't, <a href="/cough-test">take the test again.</a>
                </p>
            </div>
        </div>
    </div>
</div>
<div id="what-now">
    <h2 class="h-font header">What now?</h2>
    <h3 class="h-font">Your diagnosis is {diagnosisInfo.diagnosis ? "positive" : "negative"}.</h3>
    <p class="para">
        {#if diagnosisInfo.diagnosis}
        It is likely that you have COVID-19. However, if you don't think you are sick with any virus, then the test could be less accurate. Take the symptoms test at <a href="/input-symptoms">/input-symptoms</a> to tell if you are sick. If you are still unsure about the result, take a physical Covid test. If you are sure you have Covid, make sure to quarantine yourself as much as possible to stop the spread.
        {:else}
        You likely do not have COVID-19. However, if you feel this diagnosis is innacurate you may want to retake this test to make sure, and if you are still unsure you should take a physical test.
        {/if}
        <br><br><a href="https://www.cdc.gov/coronavirus/2019-ncov/index.html">Find the COVID-19 safety guidelines here.</a>
    </p>
</div>


