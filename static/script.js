// let polling = true;

// function fetchOutput() {
//     if (!polling) return;
//     fetch('/get_output')
//         .then(res => res.json())
//         .then(data => {
//             document.getElementById('output-box').innerText = data.text;
//             setTimeout(fetchOutput, 500); // Poll every 0.5s
//         });
// }

// document.getElementById('stop-btn').addEventListener('click', () => {
//     polling = false;

//     fetch('/stop', { method: 'POST' })
//         .then(() => fetch('/speak', { method: 'POST' }))
//         .then(() => {
//             document.getElementById('output-box').innerText += "\n[Speech Completed]";
//         });
// });

// window.onload = fetchOutput;
let polling = true;

function fetchOutput() {
    if (!polling) return;
    fetch('/get_output')
        .then(res => res.json())
        .then(data => {
            document.getElementById('output-box').innerText = data.text;
            setTimeout(fetchOutput, 500);
        });
}

document.getElementById('stop-btn').addEventListener('click', () => {
    polling = false;

    fetch('/stop', { method: 'POST' })
        .then(() => fetch('/speak', { method: 'POST' }))
        .then(() => {
            document.getElementById('output-box').innerText += "\n[Speech Completed]";
        });
});

document.getElementById('clear-btn').addEventListener('click', () => {
    fetch('/clear', { method: 'POST' })
        .then(() => {
            document.getElementById('output-box').innerText = "Detecting...";
            polling = true;
            fetchOutput();
        });
});

window.onload = fetchOutput;
