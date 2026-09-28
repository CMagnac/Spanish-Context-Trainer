from pathlib import Path

import pytest

from parser.vocabulary_parser import (
generate_vocabulary_id,
get_database_statistics,
parse_vocabulary_file,
validate_database,
)

# ---------------------------------------------------------------------

# Fixtures

# ---------------------------------------------------------------------

@pytest.fixture
def vocabulary_file(tmp_path: Path):
    """
    Create a temporary vocabulary TXT file for testing.
    """

    content = """cerrar

    verbo
    No permitir la entrada ni la salida de personas, vehículos, etc. de un lugar.

    No sé a qué hora cierran los bancos en Bélgica.

    lo siento

    expresión
    Expresión para pedir perdón o mostrar arrepentimiento.

    Lo siento mucho, pero no tengo aspirinas en casa.
    """

    filepath = tmp_path / "test_vocabulary.txt"
    filepath.write_text(content, encoding="utf-8")

    return filepath

# ---------------------------------------------------------------------

# ID generation tests

# ---------------------------------------------------------------------

def test_generate_vocabulary_id_is_deterministic():
    """
    The same input must always generate the same ID.
    """

    id_1 = generate_vocabulary_id(
        level="A1",
        context="test-context",
        source_file="test.txt",
        word="cerrar",
    )

    id_2 = generate_vocabulary_id(
        level="A1",
        context="test-context",
        source_file="test.txt",
        word="cerrar",
    )

    assert id_1 == id_2

def test_generate_vocabulary_id_changes_when_input_changes():
    """
    Different vocabulary entries should generate different IDs.
    """

    id_1 = generate_vocabulary_id(
        level="A1",
        context="test-context",
        source_file="test.txt",
        word="cerrar",
    )

    id_2 = generate_vocabulary_id(
        level="A1",
        context="test-context",
        source_file="test.txt",
        word="abrir",
    )

    assert id_1 != id_2

def test_generate_vocabulary_id_normalizes_word():
    """
    Leading/trailing spaces and capitalization should not
    change the generated ID.
    """

    id_1 = generate_vocabulary_id(
        level="A1",
        context="test-context",
        source_file="test.txt",
        word="cerrar",
    )

    id_2 = generate_vocabulary_id(
        level="A1",
        context="test-context",
        source_file="test.txt",
        word="  CERRAR  ",
    )

    assert id_1 == id_2

# ---------------------------------------------------------------------

# Vocabulary parser tests

# ---------------------------------------------------------------------

def test_parse_vocabulary_file(vocabulary_file):
    """
    The parser should correctly extract vocabulary entries.
    """

    entries = parse_vocabulary_file(
        filepath=vocabulary_file,
        level="A1",
        context="test-context",
    )

    assert len(entries) == 2

    first = entries[0]

    assert first["word"] == "cerrar"
    assert first["type"] == "verbo"
    assert (
        first["definition"]
        == "No permitir la entrada ni la salida de personas, vehículos, etc. de un lugar."
    )
    assert (
        first["example"]
        == "No sé a qué hora cierran los bancos en Bélgica."
    )

    assert first["level"] == "A1"
    assert first["context"] == "test-context"
    assert first["source_file"] == "test_vocabulary.txt"

    second = entries[1]

    assert second["word"] == "lo siento"
    assert second["type"] == "expresión"

def test_parse_vocabulary_file_generates_ids(vocabulary_file):
    """
    Every parsed vocabulary entry must contain an ID.
    """

    entries = parse_vocabulary_file(
        filepath=vocabulary_file,
        level="A1",
        context="test-context",
    )

    for entry in entries:
        assert "id" in entry
        assert entry["id"]

def test_parse_multiline_definition_and_example(tmp_path):
    """
    Definitions and examples may contain multiple lines.
    """

    content = """trabajar

    verbo
    Realizar una actividad.
    Tener una profesión.

    Trabajo en una farmacia.
    Trabajo todos los días.
    """

    filepath = tmp_path / "multiline.txt"
    filepath.write_text(content, encoding="utf-8")

    entries = parse_vocabulary_file(
        filepath=filepath,
        level="A1",
        context="test-context",
    )

    assert len(entries) == 1

    entry = entries[0]

    assert (
        entry["definition"]
        == "Realizar una actividad. Tener una profesión."
    )

    assert (
        entry["example"]
        == "Trabajo en una farmacia. Trabajo todos los días."
    )

# ---------------------------------------------------------------------

# Database validation tests

# ---------------------------------------------------------------------

def test_validate_database_accepts_unique_ids():
    """
    A database containing unique IDs should pass validation.
    """

    database = {
        "A1": {
            "test-context": [
                {
                    "id": "id-1",
                    "word": "cerrar",
                },
                {
                    "id": "id-2",
                    "word": "abrir",
                },
            ]
        }
    }

    assert validate_database(database) is True

def test_validate_database_rejects_missing_id():
    """
    An entry without an ID should raise ValueError.
    """

    database = {
        "A1": {
            "test-context": [
                {
                    "word": "cerrar",
                }
            ]
        }
    }

    with pytest.raises(ValueError, match="Missing ID"):
        validate_database(database)

def test_validate_database_rejects_duplicate_ids():
    """
    Duplicate vocabulary IDs should raise ValueError.
    """

    database = {
        "A1": {
            "test-context": [
                {
                    "id": "duplicate-id",
                    "word": "cerrar",
                },
                {
                    "id": "duplicate-id",
                    "word": "abrir",
                },
            ]
        }
    }

    with pytest.raises(
        ValueError,
        match="Duplicate vocabulary ID",
    ):
        validate_database(database)

# ---------------------------------------------------------------------

# Statistics tests

# ---------------------------------------------------------------------

def test_get_database_statistics():
    """
    Database statistics should correctly count levels,
    contexts, files, and entries.
    """

    database = {
        "A1": {
            "context-1": [
                {
                    "id": "id-1",
                    "level": "A1",
                    "context": "context-1",
                    "source_file": "file1.txt",
                },
                {
                    "id": "id-2",
                    "level": "A1",
                    "context": "context-1",
                    "source_file": "file1.txt",
                },
            ],
            "context-2": [
                {
                    "id": "id-3",
                    "level": "A1",
                    "context": "context-2",
                    "source_file": "file2.txt",
                }
            ],
        }
    }

    stats = get_database_statistics(database)

    assert stats["levels"] == 1
    assert stats["contexts"] == 2
    assert stats["files"] == 2
    assert stats["entries"] == 3
