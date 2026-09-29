// =========================================================
// SPANISH CONTEXT TRAINER
// Vocabulary module
// =========================================================


// =========================================================
// CONFIGURATION
// =========================================================

const VOCABULARY_FILE = "../data/processed/vocabulary.json";

// =========================================================
// DOM ELEMENTS
// =========================================================

const vocabularyList = document.getElementById("vocabulary-list");
const resultsCount = document.getElementById("results-count");
const emptyState = document.getElementById("empty-state");


// =========================================================
// VOCABULARY DATA
// =========================================================

let vocabularyDatabase = {};

let vocabularyEntries = [];


// =========================================================
// LOAD VOCABULARY JSON
// =========================================================

async function loadVocabulary() {

    try {

        console.log("Loading vocabulary...");

        const response = await fetch(VOCABULARY_FILE);


        // -----------------------------------------------------
        // Check HTTP response
        // -----------------------------------------------------

        if (!response.ok) {

            throw new Error(
                `HTTP error: ${response.status}`
            );

        }


        // -----------------------------------------------------
        // Convert JSON response
        // -----------------------------------------------------

        vocabularyDatabase = await response.json();


        // -----------------------------------------------------
        // Convert nested database into flat array
        // -----------------------------------------------------

        vocabularyEntries = flattenVocabulary(
            vocabularyDatabase
        );


        console.log(
            `Vocabulary loaded: ${vocabularyEntries.length} entries`
        );


        // -----------------------------------------------------
        // Display vocabulary
        // -----------------------------------------------------

        displayVocabulary(vocabularyEntries);

    }

    catch (error) {

        console.error(
            "Unable to load vocabulary:",
            error
        );

        showVocabularyError();

    }

}


// =========================================================
// FLATTEN VOCABULARY DATABASE
// =========================================================

function flattenVocabulary(database) {

    const entries = [];


    // -----------------------------------------------------
    // Level
    // -----------------------------------------------------

    for (const level in database) {

        const contexts = database[level];


        // -------------------------------------------------
        // Context
        // -------------------------------------------------

        for (const context in contexts) {

            const vocabulary = contexts[context];


            // ---------------------------------------------
            // Vocabulary entries
            // ---------------------------------------------

            vocabulary.forEach((entry) => {

                entries.push(entry);

            });

        }

    }


    return entries;

}


// =========================================================
// DISPLAY VOCABULARY
// =========================================================

function displayVocabulary(entries) {

    vocabularyList.innerHTML = "";


    // -----------------------------------------------------
    // Empty result
    // -----------------------------------------------------

    if (entries.length === 0) {

        emptyState.classList.remove("hidden");

        resultsCount.textContent =
            "No vocabulary found.";

        return;

    }


    // -----------------------------------------------------
    // Hide empty state
    // -----------------------------------------------------

    emptyState.classList.add("hidden");


    // -----------------------------------------------------
    // Update result count
    // -----------------------------------------------------

    resultsCount.textContent =
        `${entries.length} vocabulary entries`;


    // -----------------------------------------------------
    // Create cards
    // -----------------------------------------------------

    entries.forEach((entry) => {

        const card = createVocabularyCard(entry);

        vocabularyList.appendChild(card);

    });

}


// =========================================================
// CREATE VOCABULARY CARD
// =========================================================

function createVocabularyCard(entry) {

    const article = document.createElement("article");

    article.className = "vocabulary-card";


    // -----------------------------------------------------
    // Word
    // -----------------------------------------------------

    const word = document.createElement("h2");

    word.textContent = entry.word;


    // -----------------------------------------------------
    // Word type
    // -----------------------------------------------------

    const type = document.createElement("span");

    type.className = "word-type";

    type.textContent = entry.type;


    // -----------------------------------------------------
    // Definition
    // -----------------------------------------------------

    const definition = document.createElement("p");

    definition.className = "definition";

    definition.textContent = entry.definition;


    // -----------------------------------------------------
    // Example
    // -----------------------------------------------------

    const example = document.createElement("p");

    example.className = "example";

    example.textContent = entry.example;


    // -----------------------------------------------------
    // Assemble card
    // -----------------------------------------------------

    article.appendChild(word);

    article.appendChild(type);

    article.appendChild(definition);

    article.appendChild(example);


    return article;

}


// =========================================================
// ERROR DISPLAY
// =========================================================

function showVocabularyError() {

    vocabularyList.innerHTML = "";

    emptyState.classList.add("hidden");

    resultsCount.textContent =
        "Unable to load vocabulary.";

}


// =========================================================
// INITIALIZATION
// =========================================================

loadVocabulary();
