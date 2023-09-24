<script lang="ts">
    let mediaRecorder: MediaRecorder | null = null;
    let chunks: BlobPart[] = [];
    let audioURL: string = "";
    let recording: boolean = false;

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
        document.getElementById("record-button")!.className = "recording";

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
                    const audioBlob = new Blob(chunks, { type: 'audio/webm' });
                    audioURL = URL.createObjectURL(audioBlob);
                    chunks = [];
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
        document.getElementById("record-button")!.className = "";
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
</script>

<link rel="stylesheet" href="/css/cough-test.css"/>
<main>
    <div id="modal" class="invisible">
        <h3>Upload Cough</h3>
        <audio id="cough-replay" controls></audio>
        <p>
            Listen back to the audio to make sure you captured the cough clearly. Press cancel to re-record it.
        </p>
        <div>
            <button on:click={hideModal}>Cancel</button>
            <button>Submit</button>
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
