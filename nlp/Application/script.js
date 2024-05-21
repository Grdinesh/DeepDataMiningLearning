// script.js
const taskSelect = document.getElementById("task");
const textInput = document.getElementById("text-input");
const processButton = document.getElementById("process-button");
const resultText = document.getElementById("result-text");

processButton.addEventListener("click", () => {
    const task = taskSelect.value;
    const text = textInput.value;

    if (text) {
        fetch("http://localhost:8000/process", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ task, text }),
        })
        .then(response => response.json())
        .then(data => {
            resultText.textContent = data.output;
        })
        .catch(error => {
            resultText.textContent = "Error: " + error;
        });
    } else {
        resultText.textContent = "Please enter some text.";
    }
});
