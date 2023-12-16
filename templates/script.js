document.addEventListener("DOMContentLoaded", function () {
    // Display "working" message
    const statusElement = document.getElementById("status");
    statusElement.innerText = "Working...";

    // Trigger the Python script
    fetch("/generate_qr")
        .then(response => response.json())
        .then(data => {
            // Update status message
            statusElement.innerText = "Complete";

            // Display the generated QR code image
            const resultElement = document.getElementById("result");
            resultElement.src = data.output_path;
            resultElement.style.display = "block";
        })
        .catch(error => {
            console.error("Error:", error);
            statusElement.innerText = "Error";
        });

});
