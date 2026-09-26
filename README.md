# Spanish Context Trainer

A simple Spanish A1 vocabulary and grammar learning application built with Python, HTML, CSS, and JavaScript.

The project is based on contextual Spanish vocabulary and grammar material and aims to provide a practical way to explore vocabulary and practice it through interactive exercises.

## Project goals

The first version focuses on three simple features:

* **Vocabulary Explorer** — search and browse A1 vocabulary.
* **Grammar Explorer** — browse A1 grammar concepts.
* **Quiz** — practice vocabulary with interactive questions.

## Architecture

```text
spanish-context-trainer/
│
├── data/
│   ├── raw/
│   │   └── A1/
│   │
│   └── processed/
│       └── vocabulary.json
│
├── parser/
│   └── vocabulary_parser.py
│
├── web/
│   ├── index.html
│   │
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       ├── app.js
│       ├── vocabulary.js
│       └── quiz.js
│
├── tests/
│   └── test_vocabulary_parser.py
│
├── .gitignore
├── README.md
└── pyproject.toml
```

## Data pipeline

```text
Vocabulary TXT files
        │
        ▼
Python parser
        │
        ▼
vocabulary.json
        │
        ▼
HTML / CSS / JavaScript
        │
        ├── Vocabulary Explorer
        └── Quiz
```

Grammar data will follow a separate parsing process because its source files use a different structure from the vocabulary files.

## Vocabulary data

Vocabulary source files are organized by level, context, and source file.

Each parsed vocabulary entry contains:

```json
{
    "id": "...",
    "word": "...",
    "type": "...",
    "definition": "...",
    "example": "...",
    "level": "A1",
    "context": "...",
    "source_file": "..."
}
```

Vocabulary IDs are deterministic UUIDs generated from the vocabulary entry's level, context, source file, and word.

## Development roadmap

### Phase 1 — Data preparation

* [x] Define vocabulary data structure
* [x] Create vocabulary parser
* [ ] Parse the complete A1 vocabulary dataset
* [ ] Validate parsed data
* [ ] Add automated tests

### Phase 2 — Web application

* [ ] Create HTML structure
* [ ] Create application styling
* [ ] Load vocabulary JSON
* [ ] Build vocabulary search
* [ ] Add context filtering
* [ ] Add grammatical type filtering

### Phase 3 — Learning

* [ ] Create vocabulary quiz
* [ ] Add score tracking
* [ ] Store basic learning progress locally
* [ ] Improve the user interface

### Phase 4 — Grammar

* [ ] Normalize A1 grammar source files
* [ ] Create grammar parser
* [ ] Generate grammar JSON
* [ ] Build Grammar Explorer

## Technologies

* Python
* JSON
* HTML
* CSS
* JavaScript
* pytest

## Privacy and source data

The original educational source material is kept private and is not included in the public repository.

The repository contains the software used to process and present the data rather than the source educational content itself.
