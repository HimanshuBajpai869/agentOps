# AgentOps Agent Guide

## Working Rules

- Work one milestone at a time and stop for approval after each milestone.
- Analyze existing code before changing it.
- Reuse the current FastAPI, SQLAlchemy, service, and UI structure where possible.
- Before each change, state why it is needed and which files will change.
- After each milestone, report only files modified, commands to run, and expected result.

## Architecture Rules

- Keep business logic separate from storage.
- Tracer code must not import or know SQLAlchemy.
- Repositories must not contain business logic.
- Prefer service layer plus repository pattern.
- Use dependency injection where it keeps boundaries clear.
- Prefer small typed modules, Pydantic models, and SQLAlchemy models.
- Postgres is the preferred local database; keep repository boundaries compatible with SQLite for tests.

## Quality Bar

- Follow SOLID and DRY without premature abstraction.
- Prefer composition over inheritance.
- Do not rewrite working code unless the milestone requires it.
- Keep changes scoped to the milestone.
- Add tests when behavior is introduced or changed.
