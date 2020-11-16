# Contributing

## Development

- This project uses poetry for dependency management
- Unit tests can be run via running `poetry run pytest`
  - You can add `--cov` for a coverage report
  - You can add `--cov-report=html` for an HTML coverage report
- Flake8 linting can be run via running `poetry run flake8`
- All features or bug requests should be tracked against a GitHub Issue and each commit should
reference the relevant GitHub Issue(s) via `(#ID)`
- Merge requests should be to the `dev` branch
  - Make sure updates have tests where applicable (maintain coverage)
  - Make sure tests and flake8 checks are passing
