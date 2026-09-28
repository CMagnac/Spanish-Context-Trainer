from pathlib import Path
import json
import uuid


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "vocabulary.json"


# ---------------------------------------------------------------------
# ID generation
# ---------------------------------------------------------------------

def generate_vocabulary_id(
    level: str,
    context: str,
    source_file: str,
    word: str,
) -> str:
    """
    Generate a deterministic UUID for a vocabulary entry.

    The same combination of:
        level
        context
        source file
        word

    will always produce the same ID.
    """

    unique_string = (
        f"{level}/"
        f"{context}/"
        f"{source_file}/"
        f"{word.lower().strip()}"
    )

    return str(
        uuid.uuid5(
            uuid.NAMESPACE_URL,
            unique_string,
        )
    )


# ---------------------------------------------------------------------
# Vocabulary file parser
# ---------------------------------------------------------------------

def parse_vocabulary_file(
    filepath: Path,
    level: str,
    context: str,
):
    """
    Parse one vocabulary TXT file.

    Expected structure:

        word

        grammar
        definition

        example

        word

        grammar
        definition

        example
    """

    with filepath.open("r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    entries = []

    i = 0

    # Filename used as source metadata
    source_file = filepath.name

    while i < len(lines):

        # -------------------------------------------------------------
        # Skip blank lines
        # -------------------------------------------------------------

        while i < len(lines) and lines[i].strip() == "":
            i += 1

        if i >= len(lines):
            break

        # -------------------------------------------------------------
        # Word
        # -------------------------------------------------------------

        word = lines[i].strip()
        i += 1

        if not word:
            continue

        # -------------------------------------------------------------
        # Skip blank lines
        # -------------------------------------------------------------

        while i < len(lines) and lines[i].strip() == "":
            i += 1

        if i >= len(lines):
            break

        # -------------------------------------------------------------
        # Grammar / word type
        # -------------------------------------------------------------

        word_type = lines[i].strip()
        i += 1

        if not word_type:
            continue

        # -------------------------------------------------------------
        # Definition
        #
        # The definition may contain several lines.
        # It ends at the next blank line.
        # -------------------------------------------------------------

        definition_lines = []

        while i < len(lines) and lines[i].strip() != "":
            definition_lines.append(lines[i].strip())
            i += 1

        definition = " ".join(definition_lines)

        # -------------------------------------------------------------
        # Skip blank lines
        # -------------------------------------------------------------

        while i < len(lines) and lines[i].strip() == "":
            i += 1

        # -------------------------------------------------------------
        # Example
        #
        # The example may contain several lines.
        # It ends at the next blank line.
        # -------------------------------------------------------------

        example_lines = []

        while i < len(lines) and lines[i].strip() != "":
            example_lines.append(lines[i].strip())
            i += 1

        example = " ".join(example_lines)

        # -------------------------------------------------------------
        # Generate stable ID
        # -------------------------------------------------------------

        entry_id = generate_vocabulary_id(
            level=level,
            context=context,
            source_file=source_file,
            word=word,
        )

        # -------------------------------------------------------------
        # Create vocabulary entry
        # -------------------------------------------------------------

        entry = {
            "id": entry_id,
            "word": word,
            "type": word_type,
            "definition": definition,
            "example": example,
            "level": level,
            "context": context,
            "source_file": source_file,
        }

        entries.append(entry)

    return entries


# ---------------------------------------------------------------------
# Build JSON database
# ---------------------------------------------------------------------

def build_database():

    database = {}

    if not RAW_DIR.exists():
        raise FileNotFoundError(
            f"Raw data directory not found: {RAW_DIR}"
        )

    # -----------------------------------------------------------------
    # Level
    # -----------------------------------------------------------------

    for level_dir in sorted(RAW_DIR.iterdir()):

        if not level_dir.is_dir():
            continue

        level = level_dir.name

        database[level] = {}

        # -------------------------------------------------------------
        # Context
        # -------------------------------------------------------------

        for context_dir in sorted(level_dir.iterdir()):

            if not context_dir.is_dir():
                continue

            context = context_dir.name

            # ---------------------------------------------------------
            # Vocabulary directory
            # ---------------------------------------------------------

            vocab_dir = context_dir / "vocabulaire"

            if not vocab_dir.exists():
                continue

            if not vocab_dir.is_dir():
                continue

            database[level][context] = []

            # ---------------------------------------------------------
            # Vocabulary TXT files
            # ---------------------------------------------------------

            for txt_file in sorted(vocab_dir.glob("*.txt")):

                print(
                    f"Parsing: "
                    f"{level}/{context}/{txt_file.name}"
                )

                entries = parse_vocabulary_file(
                    filepath=txt_file,
                    level=level,
                    context=context,
                )

                database[level][context].extend(entries)

    return database


# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

def validate_database(database):
    """
    Check that every vocabulary entry has a unique ID.
    """

    ids = set()

    for level, contexts in database.items():

        for context, entries in contexts.items():

            for entry in entries:

                entry_id = entry.get("id")

                if not entry_id:
                    raise ValueError(
                        f"Missing ID for vocabulary entry: "
                        f"{entry}"
                    )

                if entry_id in ids:
                    raise ValueError(
                        f"Duplicate vocabulary ID detected: "
                        f"{entry_id}"
                    )

                ids.add(entry_id)

    return True


# ---------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------

def get_database_statistics(database):

    total_entries = 0
    total_levels = len(database)
    total_contexts = 0
    total_files = set()

    for level, contexts in database.items():

        total_contexts += len(contexts)

        for context, entries in contexts.items():

            total_entries += len(entries)

            for entry in entries:
                total_files.add(
                    (
                        entry["level"],
                        entry["context"],
                        entry["source_file"],
                    )
                )

    return {
        "levels": total_levels,
        "contexts": total_contexts,
        "files": len(total_files),
        "entries": total_entries,
    }


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():

    print("=" * 60)
    print("SPANISH CONTEXT TRAINER")
    print("Vocabulary parser")
    print("=" * 60)

    print(f"\nRaw data:")
    print(RAW_DIR)

    print(f"\nOutput:")
    print(OUTPUT_FILE)

    # -------------------------------------------------------------
    # Build database
    # -------------------------------------------------------------

    database = build_database()

    # -------------------------------------------------------------
    # Validate
    # -------------------------------------------------------------

    validate_database(database)

    # -------------------------------------------------------------
    # Create output directory
    # -------------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # -------------------------------------------------------------
    # Save JSON
    # -------------------------------------------------------------

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            database,
            f,
            indent=4,
            ensure_ascii=False,
        )

    # -------------------------------------------------------------
    # Statistics
    # -------------------------------------------------------------

    stats = get_database_statistics(database)

    print("\n" + "=" * 60)
    print("PARSING COMPLETED")
    print("=" * 60)

    print(f"Levels:   {stats['levels']}")
    print(f"Contexts: {stats['contexts']}")
    print(f"Files:    {stats['files']}")
    print(f"Entries:  {stats['entries']}")

    print(f"\nJSON written to:")
    print(OUTPUT_FILE)


# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------

if __name__ == "__main__":
    main()
