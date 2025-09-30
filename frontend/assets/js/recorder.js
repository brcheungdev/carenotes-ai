let mediaRecorder = null;
let chunks = [];
let currentStream = null;

export async function startRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        return;
    }
    currentStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(currentStream);
    chunks = [];
    mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
            chunks.push(event.data);
        }
    };
    mediaRecorder.start();
}

export function isRecording() {
    return mediaRecorder?.state === 'recording';
}

export function stopRecording() {
    return new Promise((resolve, reject) => {
        if (!mediaRecorder) {
            reject(new Error('not_recording'));
            return;
        }
        mediaRecorder.onstop = () => {
            const blob = new Blob(chunks, { type: mediaRecorder.mimeType || 'audio/webm' });
            if (currentStream) {
                currentStream.getTracks().forEach((track) => track.stop());
                currentStream = null;
            }
            resolve(blob);
        };
        mediaRecorder.stop();
    });
}
