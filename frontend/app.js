async function analyze() {

    let text = document.getElementById("inputText").value;

    const file = document.getElementById("fileInput").files[0];

    if (file) {
        text = await file.text();
    }

    const response = await fetch("http://127.0.0.1:5000/process", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: text })
    });

    const data = await response.json();

    document.getElementById("result").innerHTML =
        JSON.stringify(data, null, 2);
}