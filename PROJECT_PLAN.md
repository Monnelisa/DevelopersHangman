# Project Plan

This plan outlines a practical path to evolve Developers Hangman into a polished portfolio project.

## Phase 1: Professional polish (1-2 days)

- Add a CLI with flags: `--seed`, `--questions`, `--language`, `--difficulty`.
- Update README with CLI usage examples and a short “Design Decisions” section.
- Add `ruff` for lint + format with a `pyproject.toml`.

## Phase 2: Testing depth (1-2 days)

- Add input-simulation tests using `pytest` + `monkeypatch`.
- Add edge-case tests: invalid JSON, empty question bank, repeated guesses.
- Add coverage reporting (optional).

## Phase 3: Product-level usability (2-3 days)

- Add replay prompt and graceful exit.
- Add level summary stats (accuracy, attempts, best streak).
- Add optional hints with score penalty.

## Phase 4: Packaging and distribution (2-3 days)

- Add packaging config with `pyproject.toml`.
- Create a console entry point (`hangman`).
- Document how to install in editable mode and run the CLI.

## Phase 5: Visual demo and docs (1 day)

- Add screenshots or a short GIF to the README.
- Document JSON schema and how to add new question banks.
