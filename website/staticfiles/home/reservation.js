// Existing JavaScript in base.js

// Reservation Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const tables = document.querySelectorAll(".table");
    const selectedTableInput = document.getElementById("selectedTable"); // Hidden input in Django form
    let selectedTable = null;

    tables.forEach(table => {
        table.addEventListener("click", () => {
            tables.forEach(t => t.classList.remove("selected"));
            table.classList.add("selected");
            selectedTable = table.dataset.table;
            selectedTableInput.value = selectedTable; // Set the value of the hidden input
        });
    });

    // The confirmation box should ideally be shown *after* a successful Django form submission.
    // We can use Django messages to trigger it, or use AJAX for a more seamless experience.
    // For now, let's keep the form submission as is and manage the confirmation box visually.

    // If you want the JS-driven confirmation box:
    const bookingForm = document.getElementById("bookingForm");
    const confirmationBox = document.getElementById("confirmationBox");

    if (bookingForm) {
        bookingForm.addEventListener("submit", function(e) {
            // Do NOT prevent default here if you want Django to handle the form submission.
            // e.preventDefault(); // Keep commented out for Django form submission

            if (!selectedTableInput.value) { // Check if the hidden input has a value
                alert("Please select a table before booking.");
                e.preventDefault(); // Prevent form submission if no table is selected
                return;
            }

            // If Django successfully processes the form and redirects with a success message,
            // you can add logic to check for that message and then show the confirmation box.
            // This part is trickier without AJAX.

            // For demonstration of the pop-up without Django form submission (NOT RECOMMENDED for final):
            // document.getElementById("confirmationBox").classList.add("show");
            // this.reset(); // Resets the form after visual confirmation (but Django already handles it)
            // tables.forEach(t => t.classList.remove("selected"));
            // selectedTable = null;
        });
    }

    // Function to show the confirmation box based on Django messages
    // This will run when the page reloads after a successful submission
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('reservation_success') === 'true') {
        confirmationBox.classList.add('show');
        // Optionally, remove the success parameter from URL
        history.replaceState({}, document.title, window.location.pathname);
    }
});

// Function to close the confirmation box
function closeConfirmationBox() {
    document.getElementById('confirmationBox').classList.remove('show');
}