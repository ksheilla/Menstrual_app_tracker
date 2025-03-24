document.addEventListener("DOMContentLoaded", function () {
    let cycleDates = [];

    // Handle form submission
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
        let historyList = document.getElementById("cycle-history");
        historyList.innerHTML = "";

        cycleDates.forEach((date, index) => {
            let li = document.createElement("li");
            li.textContent = date.toDateString();
            li.onclick = () => removeDate(index); // Allow clicking to remove a date
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
            document.getElementById("next-period").textContent = "Not enough data for prediction.";
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

        document.getElementById("next-period").textContent = `Next predicted period: ${nextPeriod.toDateString()}`;
    }
});
