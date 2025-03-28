document.addEventListener("DOMContentLoaded", function () {
    let cycleDates = [];

    // Elements
    const historyList = document.getElementById("cycle-history");
    const nextPeriodText = document.getElementById("next-period");
    const recommendationsContainer = document.getElementById("recommendations");
    const recommendationsLink = document.getElementById("recommendations-link");

    /** 🩸 HANDLE CYCLE TRACKING **/
    document.getElementById("cycle-form").addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent page refresh
        let dateInput = document.getElementById("start_date").value;
        if (dateInput) {
            let date = new Date(dateInput);
            if (!isNaN(date.getTime())) {
                cycleDates.push(date);
                cycleDates.sort((a, b) => a - b); // Keep dates sorted
                updateCycleHistory();
                predictNextPeriod();
            } else {
                alert("Invalid date format. Please enter a valid date.");
            }
        }
    });

    function updateCycleHistory() {
        historyList.innerHTML = "";
        cycleDates.forEach((date, index) => {
            let li = document.createElement("li");
            li.textContent = date.toDateString();
            li.onclick = () => removeDate(index); // Click to remove a date
            historyList.appendChild(li);
        });
    }

    function removeDate(index) {
        if (confirm("Remove this date?")) {
            cycleDates.splice(index, 1);
            updateCycleHistory();
            predictNextPeriod();
        }
    }

    function predictNextPeriod() {
        if (cycleDates.length < 2) {
            nextPeriodText.textContent = "Not enough data for prediction.";
            return;
        }
        
        let cycleLengths = [];
        for (let i = 1; i < cycleDates.length; i++) {
            let diff = (cycleDates[i] - cycleDates[i - 1]) / (1000 * 60 * 60 * 24);
            cycleLengths.push(diff);
        }

        let avgCycleLength = Math.round(cycleLengths.reduce((a, b) => a + b, 0) / cycleLengths.length);
        let lastPeriod = cycleDates[cycleDates.length - 1];
        let nextPeriod = new Date(lastPeriod);
        nextPeriod.setDate(lastPeriod.getDate() + avgCycleLength);

        nextPeriodText.textContent = `Next predicted period: ${nextPeriod.toDateString()}`;
    }

    /** 🍽️ FETCH NUTRITION RECOMMENDATIONS **/
    function fetchRecommendations(phase) {
        fetch(`/recommendations/${phase}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    recommendationsContainer.innerHTML = `<p>${data.error}</p>`;
                    return;
                }

                let html = `
                    <h2>🍽️ Personalized Nutrition Recommendations</h2>
                    <div class="recipe-recommendations">
                        ${data.map(recipe => `
                            <div class="recipe-card">
                                <img src="${recipe.image}" alt="${recipe.title}">
                                <h3>${recipe.title}</h3>
                                <div class="recipe-details">
                                    <p><strong>Nutritional Focus:</strong> ${recipe.nutritionalTag}</p>
                                    <p><strong>Phase Benefits:</strong> ${recipe.phaseBenefits}</p>
                                    <details>
                                        <summary>View Preparation</summary>
                                        <p>${recipe.instructions}</p>
                                    </details>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                `;
                recommendationsContainer.innerHTML = html;
            })
            .catch(error => {
                console.error("Error fetching recommendations:", error);
                recommendationsContainer.innerHTML = "<p>Failed to fetch recommendations. Please try again later.</p>";
            });
    }

    // Add Click Event for Recommendations
    if (recommendationsLink) {
        recommendationsLink.addEventListener("click", function (e) {
            e.preventDefault();
            fetchRecommendations("menstruation"); // Default phase for now
        });
    }
});
