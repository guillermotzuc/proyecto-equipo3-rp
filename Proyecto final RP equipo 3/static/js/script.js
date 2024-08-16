let mediaRecorder;
let audioChunks = [];

document.getElementById("record-btn").addEventListener("click", async function() {
    let stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.start();
    document.getElementById("record-btn").disabled = true;
    document.getElementById("stop-btn").disabled = false;

    mediaRecorder.ondataavailable = function(event) {
        audioChunks.push(event.data);
    };
});

document.getElementById("stop-btn").addEventListener("click", function() {
    mediaRecorder.stop();
    document.getElementById("record-btn").disabled = false;
    document.getElementById("stop-btn").disabled = true;

    mediaRecorder.onstop = function() {
        let blob = new Blob(audioChunks, { type: 'audio/wav' });
        let audioUrl = URL.createObjectURL(blob);
        let audio = document.getElementById("audio");
        audio.src = audioUrl;

        let formData = new FormData();
        formData.append('audio', blob, 'audio.wav');

        fetch('/upload_audio', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("text-output").textContent = data.text;
            document.getElementById("image-output").src = data.image_url;
        })
        .catch(error => {
            console.error("Error:", error);
        });

        audioChunks = []; // Limpiar los chunks para la próxima grabación
    };
});
