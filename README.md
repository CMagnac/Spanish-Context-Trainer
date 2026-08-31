# Spanish Context Trainer 🇪🇸

A Python-based Spanish learning system built around **contextual vocabulary, RAG, AI agents, and personalized learning**.

The project is designed to transform structured Spanish vocabulary resources into a database that an AI agent can use to generate exercises.

## 🎯 Project Goals

The main objective is to build a Spanish learning assistant.

Instead of giving the AI model the entire vocabulary dataset, the system will use **Retrieval-Augmented Generation (RAG)** to retrieve only the vocabulary relevant to the current learning task.

The project follows a **modular architecture** inspired by **MVC**.

## Repository Structure

The planned project structure is :

```text
SPANISH-CONTEXT-TRAINER/
│
├── src/
│   └── spanish_trainer/
│       │
│       ├── config/
│       │
│       ├── models/
│       │
│       ├── parsers/
│       │
│       ├── repositories/
│       │
│       ├── embeddings/
│       │
│       ├── vectorstore/
│       │
│       ├── rag/
│       │
│       ├── agent/
│       │
│       ├── services/
│       │
│       ├── controllers/
│       │
│       └── main.py
│
├── scripts/
│   ├── import_vocabulary.py
│   ├── build_embeddings.py
│   └── rebuild_vectorstore.py
│
├── tests/
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── embeddings/
│   ├── vectorstore/
│   └── learning/
│
├── notebooks/
│
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
└── pyproject.toml
```

## Data Pipeline

The vocabulary pipeline is designed as :

```text
TXT files
   │
   ▼
Parser
   │
   ▼
Structured vocabulary
   │
   ▼
JSON
   │
   ▼
Embeddings
   │
   ▼
Vector Store
```

A vocabulary entry is represented as :

```json
{
    "id": "6b87f542-f418-5ce8-9029-093885941f72",
    "word": "cerrar",
    "type": "verbo",
    "definition": "...",
    "example": "...",
    "level": "A1",
    "context": "comprar-comida",
    "source_file": "myfile.txt"
}
```

The stable `id` allows the same vocabulary item to be referenced by the JSON dataset, vector store, and learning database.

## RAG

The system will use **Retrieval-Augmented Generation** rather than placing the complete vocabulary database inside an LLM prompt.

The agent can use that retrieved context to construct an appropriate exercise.

## AI Agent

The AI agent is intended to coordinate several specialized components :

* Exercise generation ;
* Answer correction ;
* Difficulty selection ;
* Learning state.

This information will eventually be used for adaptive learning and spaced repetition.

## Data Privacy & Copyright

The project may use vocabulary material obtained from third-party educational resources for **personal study and development**.

Third-party educational content is **not included in this public repository**.

Private data may include:

```text
data/raw/
data/processed/
data/embeddings/
data/vectorstore/
data/learning/
```

These directories are excluded from version control.

The public repository contains the application code and architecture, while private educational data remains local.

## Project Development

The project is being developed incrementally.
The goal is to keep each component independent and testable.

## Planned Technology Stack

The exact technologies may evolve during development.

### Core

* Python
* `pathlib`
* `json`
* `dataclasses` / Pydantic
* pytest

### Data

* JSON during the initial development phase
* SQLite for learner progress
* Vector database for semantic retrieval

### AI

* Embedding model
* Large Language Model
* RAG pipeline
* AI agent

### Possible future interfaces

* CLI
* Web application
* Streamlit interface

## License

Third-party educational content is **not part of this repository** and remains subject to its original copyright and licensing conditions.
