# Contributing

## Before coding

Open an issue first to discuss the approach. This helps avoid wasted effort and gives maintainers a chance to provide guidance.

## Structure

This is a UV workspace monorepo with two packages:

- `packages/migra` — schema diff and migration generation
- `packages/schemainspect` — PostgreSQL schema introspection

Most features require changes to both packages. `schemainspect` handles database introspection, `migra` handles diffing and SQL generation.

## Development

```bash
just install    # install dependencies
just test       # run all tests (requires local PostgreSQL)
just lint       # run linter
just fmt        # format code
```

## Pull requests

- Keep PRs small and focused — ideally under 200 lines
- Add tests for new functionality
- Run `just check` before submitting
- If your change touches schema introspection, add a test fixture in `packages/migra/tests/FIXTURES/`
