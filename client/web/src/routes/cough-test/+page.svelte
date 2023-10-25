<script lang="ts">
    import axios from 'axios';

    import { coughTestOptionLabels } from '$lib/coughTestOptions';

    let mediaRecorder: MediaRecorder | null = null;
    let chunks: BlobPart[] = [];
    let audioURL: string = "";
    let recording: boolean = false;
    let audioBlob: Blob | null = null;

    export function handleCheck(e: Event) {
        (document.getElementsByClassName((e.target as HTMLInputElement).dataset["name"]!)[0] as HTMLInputElement).value = (e.target as HTMLInputElement).checked.toString()
    }

    export async function handleRecordButtonClick() {
        if (recording) {
            stopRecording();
        }
        else {
            startRecording();
        }
        recording = !recording;
    }

    export function startRecording() {
        document.getElementById("record")!.className = "recording";

        chunks = [];

        navigator.mediaDevices
            .getUserMedia({ audio: true })
            .then((stream) => {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        chunks.push(event.data);
                    }
                };

                mediaRecorder.onstop = () => {
                    audioBlob = new Blob(chunks, { type: 'audio/wav' });
                    audioURL = URL.createObjectURL(audioBlob);
                    showModal();
                };

                mediaRecorder.start();
            })
            .catch((error) => {
                console.error('Error accessing the microphone:', error);
            });
    }

    export function stopRecording() {
        if (mediaRecorder) {
            mediaRecorder.stop();
            mediaRecorder = null;
        }
    }

    export function showModal() {
        document.getElementById("record")!.className = "";
        const modal = document.getElementById("modal");
        if (modal) {
            modal.className = "visible";
        }

        (document.getElementById("cough-replay") as HTMLAudioElement).src = audioURL;
    }

    export function hideModal() {
        const modal = document.getElementById("modal");
        if (modal) {
            modal.className = "invisible";
        }
    }

    export async function postCough() {
        const formData = new FormData(document.getElementById("cough-questions") as HTMLFormElement);
        let coughTestOptions: any = {};
        formData.forEach((value, key) => {
            coughTestOptions[key] = value
        });

        let pageData = {
            diagnosisInfo: {},
            coughTestOptions
        }

        const response = await fetch("https://143.42.118.185:5000/upload", {
            headers: {
                'Content-Type': 'audio/wav',
            },
            body: audioBlob,
            method: "POST"
        })
        if (response.ok) {
            const responseData = await response.json();

            pageData.diagnosisInfo = {...responseData, type: "cough"};
            window.location.href = `/diagnosis/${encodeURIComponent(JSON.stringify(pageData))}`
        }
    }
</script>

<link rel="stylesheet" href="/css/cough-test.css"/>
<main>
    <div id="modal" class="invisible">
        <h3>Upload Cough</h3>
        <audio id="cough-replay" controls></audio>
        <p>
            Listen back to the audio to make sure you captured the cough clearly. Press cancel to re-record it.
        </p>
        <form id="cough-questions">
            {#each coughTestOptionLabels as [coughTestOptionLabel, propertyName]}
            <div>
                <label for={propertyName}>{coughTestOptionLabel}</label>
                <div>
                    {#if coughTestOptionLabel.includes("[")}
                    <select name={propertyName}>
                        {#each coughTestOptionLabel.substring(
                        coughTestOptionLabel.indexOf("[") + 1,
                        coughTestOptionLabel.indexOf("]")
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
        </form>
        <div>
            <button on:click={hideModal}>Cancel</button>
            <button on:click={() => {hideModal(); postCough()}}>Submit</button>
        </div>
    </div>
    <div id="record">
        <button id="record-button" on:click={handleRecordButtonClick}></button>
        <div id="record-button-effect">

        </div>
    </div>
    <div id="description">
        <h1>Record Cough</h1> 
        <p>
            Press the button when you are ready, press again to stop
            <br><br>
            If you aren't satisfied with the quality of the recording, you can discard the recording and redo it. Make sure the cough is natural and not forced.
        </p> 
    </div>
</main>
