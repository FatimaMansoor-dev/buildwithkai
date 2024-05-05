const prevBtns = document.querySelectorAll(".btn-prev");
const nextBtns = document.querySelectorAll(".btn-next");
const progress = document.getElementById("progress");
const formSteps = document.querySelectorAll(".form-step");
const progressSteps = document.querySelectorAll(".progress-step");

let formStepsNum = 0;

// Function to fetch the estimated budget from the server
function fetchEstimatedBudget() {
    // Make a request to the server to get the estimated budget
    fetch('/get_estimated_budget')
        .then(response => response.text())
        .then(data => {
            // Update the content of the span element with the estimated budget
            document.getElementById('estimatedBudget').textContent = data;
        })
        .catch(error => console.error('Error fetching estimated budget:', error));
}

// Call the fetchEstimatedBudget function when the page loads
window.onload = fetchEstimatedBudget;

// Function to validate input fields before proceeding to the next step
function validateInputFields() {
    // Get the input values
    const location = document.getElementById("location").value;
    const destination = document.getElementById("destination").value;

    // Check if any of the fields is empty
    if (location.trim() === '' || destination.trim() === '') {
        // If any field is empty, display an alert message
        alert("Please fill in all fields before proceeding.");
        return false;
    }

    // If all fields are filled, return true to allow the form to proceed
    return true;
}

nextBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
        // Validate input fields before proceeding
        if (!validateInputFields()) {
            // If validation fails, do not proceed
            return;
        }

        // Get user's location and destination
        const location = document.getElementById("location").value;
        const destination = document.getElementById("destination").value;

        // Send location and destination data to the server
        fetch('/get_estimated_budget', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ location: location, destination: destination }),
        })
        .then(response => response.text())
        .then(data => {
            // Update the content of the span element with the estimated budget
            document.getElementById('estimatedBudget').textContent = data;
        })
        .catch(error => console.error('Error fetching estimated budget:', error));

        formStepsNum++;
        updateFormSteps();
        updateProgressbar();
    });
});

prevBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
        formStepsNum--;
        updateFormSteps();
        updateProgressbar();
    });
});

function updateFormSteps() {
    formSteps.forEach((formStep) => {
        formStep.classList.contains("form-step-active") &&
            formStep.classList.remove("form-step-active");
    });

    formSteps[formStepsNum].classList.add("form-step-active");
}

function updateProgressbar() {
    progressSteps.forEach((progressStep, idx) => {
        if (idx < formStepsNum + 1) {
            progressStep.classList.add("progress-step-active");
        } else {
            progressStep.classList.remove("progress-step-active");
        }
    });

    const progressActive = document.querySelectorAll(".progress-step-active");

    progress.style.width =
        ((progressActive.length - 1) / (progressSteps.length - 1)) * 100 + "%";
}
// Update the selector for the submit button to match its class and type
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('.form');
    const submitBtn = form.querySelector('input[type="submit"]');

    submitBtn.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default form submission
        // Get the user-entered budget
        const userBudget = parseFloat(document.getElementById('budget').value);

        // Get the estimated budget text
        const estimatedBudgetText = document.getElementById('estimatedBudget').textContent;

        // Split the estimated budget text by ":"
        const estimatedBudgetArray = estimatedBudgetText.split(':')[1];
        // Extract the budget value from the array and convert it to a number
        const estimatedBudget = parseFloat(estimatedBudgetArray[1]);
        const estimatedBudgetValue = parseFloat(estimatedBudgetText.replace(/\D/g, ''));

        console.log(estimatedBudgetValue);
        // Compare the user-entered budget with the estimated budget
        if (userBudget < estimatedBudgetValue) {
            alert('Your budget is insufficient!');
            // You can redirect to the next step or perform any other action here
        } else {
            // Accessing input values
            const location = form.querySelector('#location').value;
            const days = form.querySelector('#destination').value;
            const area = form.querySelector('select[name="hotels"]').value;
            const timeOfTravel = form.querySelector('#timeOfTravel').value;
            const budget = form.querySelector('#budget').value;
        
        
            // Prepare the data to send to the server
            const formData = {
                location: location,
                days: days,
                area: area,
                time: timeOfTravel,
                budget: budget,
                days: days
            };
        
            // Send the data to the server
            fetch('/generate_travel_plan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            })


            .then(response => response.json())
            .then(data => {
                // Redirect to main.html page with the generated travel plan
                window.location.href = '/main?travel_plan=' + encodeURIComponent(JSON.stringify(data));
            })
            .catch(error => console.error('Error:', error));
            }
        
            

    });
});
