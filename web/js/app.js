// =========================================================
// SPANISH CONTEXT TRAINER
// Main application controller
// =========================================================


// =========================================================
// DOM ELEMENTS
// =========================================================

const navigationButtons = document.querySelectorAll(".nav-button");

const applicationSections = document.querySelectorAll(".app-section");


// =========================================================
// SECTION NAVIGATION
// =========================================================

function showSection(sectionName) {

    // -----------------------------------------------------
    // Hide all sections
    // -----------------------------------------------------

    applicationSections.forEach((section) => {
        section.hidden = true;
        section.classList.remove("active");
    });


    // -----------------------------------------------------
    // Remove active state from navigation buttons
    // -----------------------------------------------------

    navigationButtons.forEach((button) => {
        button.classList.remove("active");
    });


    // -----------------------------------------------------
    // Show selected section
    // -----------------------------------------------------

    const selectedSection = document.getElementById(
        `${sectionName}-section`
    );

    if (!selectedSection) {
        console.warn(
            `Section not found: ${sectionName}`
        );

        return;
    }

    selectedSection.hidden = false;
    selectedSection.classList.add("active");


    // -----------------------------------------------------
    // Activate corresponding navigation button
    // -----------------------------------------------------

    const selectedButton = document.querySelector(
        `.nav-button[data-section="${sectionName}"]`
    );

    if (selectedButton) {
        selectedButton.classList.add("active");
    }
}


// =========================================================
// NAVIGATION EVENTS
// =========================================================

navigationButtons.forEach((button) => {

    button.addEventListener("click", () => {

        const sectionName = button.dataset.section;

        showSection(sectionName);

    });

});


// =========================================================
// INITIAL APPLICATION STATE
// =========================================================

function initializeApplication() {

    showSection("vocabulary");

}


// =========================================================
// START APPLICATION
// =========================================================

initializeApplication();
