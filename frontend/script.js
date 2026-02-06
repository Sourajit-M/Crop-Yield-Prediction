const form = document.getElementById("predictionForm");
const resultDiv = document.getElementById("result");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        Year: parseInt(document.getElementById("year").value),
        average_rain_fall_mm_per_year: parseFloat(document.getElementById("rainfall").value),
        pesticides_tonnes: parseFloat(document.getElementById("pesticides").value),
        avg_temp: parseFloat(document.getElementById("temp").value),
        Area: document.getElementById("area").value,
        Item: document.getElementById("item").value
    };

    resultDiv.innerHTML = "⏳ Predicting...";

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        resultDiv.innerHTML = `
            🌱 Predicted Yield: <br>
            ${result.predicted_yield_hg_per_ha} hg/ha
        `;
    } catch (error) {
        resultDiv.innerHTML = "❌ Error connecting to API";
    }
});
