<script lang="ts">
  import { onMount } from "svelte";
  import { coughTestOptionLabels } from "$lib/coughTestOptions";
  import { symptomInputOptionLabels } from "$lib/symptomInputOptions";
  import type { PageData } from "./[diagnosis]/$types";

    export let data: PageData
    let diagnosisInfo: DiagnosisInfo = data.diagnosisInfo;

    let options: CoughTestOptions | SymptomInputOptions = diagnosisInfo.type == "cough" ? data.coughTestOptions : data.symptomInputOptions;
    let info: Array<Array<any>> = []
    let labels = diagnosisInfo.type == "cough" ? coughTestOptionLabels : symptomInputOptionLabels;

    function populateUserOptions() {
        let i = 0;
        for (const value of Object.values(options)) {
            if (i > labels.length) return;
            info[i] = [labels[i], value];
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
</script>

<link rel="stylesheet" href="/css/diagnosis.css"/>

<div id="container">
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


