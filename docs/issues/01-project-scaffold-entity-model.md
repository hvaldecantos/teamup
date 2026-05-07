# Issue 1: Project scaffold & Entity data model

**Type**: AFK

## What to build

Set up the `src/teamup_copilot/` package structure and implement the `Entity` data model. `Entity` wraps a named identifier and an arbitrary attributes dictionary, providing type-safe access so that attribute errors are caught early. This slice establishes the foundation that all subsequent slices build on — no algorithm or scoring logic is included here.

## Tech stack

- **Pydantic**: Use `BaseModel` for all data classes (`Entity`)
- **Type hints**: All functions and methods must carry full type annotations, passing `mypy --strict`
- **Tests**: Written with `pytest`; add `pydantic`, `mypy`, and `pytest` to `pyproject.toml` dependencies

## Acceptance criteria

- [ ] `src/teamup_copilot/` package is created with an `__init__.py` that exposes the public API surface
- [ ] `Entity` class accepts an identifier (string) and an attributes dictionary (str → numeric)
- [ ] Accessing a missing attribute raises a clear, descriptive error
- [ ] Basic unit tests cover construction, attribute access, and the missing-attribute error case

## Blocked by

None — can start immediately
