async function fetchAnnotation() {
    const transcriptId = document.getElementById("transcriptId").value;
    const cdnaPosition = document.getElementById("cdnaPosition").value;
    const genomeBuild = document.getElementById("genomeBuild").value;

    const response = await fetch("/annotate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ transcript_id: transcriptId, cdna_position: cdnaPosition, genome_build: genomeBuild })
    });

    const result = await response.json();
    if (result.error) {
        document.getElementById("result").innerHTML = `<div class="alert alert-danger">${result.error}</div>`;
    } else {
        document.getElementById("result").innerHTML = `<pre>${JSON.stringify(result, null, 2)}</pre>`;
    }
}
