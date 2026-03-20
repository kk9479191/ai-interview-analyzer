function startSpeech() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

    recognition.lang = "en-US";
    recognition.interimResults = false;

    recognition.start();

    recognition.onstart = () => {
        console.log("Listening... 🎤");
    };

    recognition.onresult = (event) => {
        const speechResult = event.results[0][0].transcript;

        document.getElementById("answer").value = speechResult;

        console.log("You said:", speechResult);
    };

    recognition.onerror = (event) => {
        console.error("Speech error:", event.error);
    };
}