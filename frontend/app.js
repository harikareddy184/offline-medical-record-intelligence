async function processData() {
  const input = document.getElementById("inputText").value;

  const response = await fetch("http://127.0.0.1:5000/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text: input })
  });

  const data = await response.json();

  document.getElementById("output").innerText =
    JSON.stringify(data, null, 2);
}
