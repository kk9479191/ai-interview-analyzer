const video = document.getElementById("video");
const emotionText = document.getElementById("emotion");

window.currentEmotion = "neutral";

async function startVideo() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;

    video.onloadedmetadata = () => {
        video.play();
        console.log("Camera Started ✅");
    };
}

async function loadModels() {
    console.log("Loading models...");   // 🔥 pehle

    await faceapi.nets.tinyFaceDetector.loadFromUri("/static/models");
    await faceapi.nets.faceExpressionNet.loadFromUri("/static/models");

    console.log("Models Loaded ✅");   // 🔥 baad me
}

function detectEmotion() {

    const canvas = faceapi.createCanvasFromMedia(video);
    document.querySelector(".video-container").append(canvas);
    // 🔥 FIX: displaySize define karo
    const displaySize = {
    width: video.offsetWidth,
    height: video.offsetHeight
};

canvas.width = video.offsetWidth;
canvas.height = video.offsetHeight;
    faceapi.matchDimensions(canvas, displaySize);

    setInterval(async () => {

        const detections = await faceapi
            .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
            .withFaceExpressions();

        const resized = faceapi.resizeResults(detections, displaySize);

        canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);

        if (resized.length > 0) {

            const expressions = resized[0].expressions;

            let maxEmotion = "neutral";
            let maxValue = 0;

            for (let key in expressions) {
                if (expressions[key] > maxValue) {
                    maxValue = expressions[key];
                    maxEmotion = key;
                }
            }

            window.currentEmotion = maxEmotion;
            emotionText.innerText = maxEmotion;

            resized.forEach(detection => {
                const box = detection.detection.box;

                const drawBox = new faceapi.draw.DrawBox(box, {
                    label: maxEmotion
                });

                drawBox.draw(canvas);
            });
        }

    }, 500);
}

async function init() {
    console.log("Init started");

    await startVideo();
    await loadModels();

    console.log("Starting detection...");

    detectEmotion();
}
init();