# Contributing

## Development

- This project uses poetry for dependency management
- All features or bug requests should be tracked against a GitHub Issue and each commit should
reference the relevant GitHub Issue(s) via `(#ID)`
- Merge requests should be to the `dev` branch
  - Make sure updates have tests where applicable (maintain coverage)
  - Make sure tests and flake8 checks are passing

### Unit Testing
- Unit tests can be run via running `poetry run pytest`
  - You can add `--cov` for a coverage report
  - You can add `--cov-report=html` for an HTML coverage report
- Make sure unit tests are passing for any merge request

### Linting
- Flake8 linting can be run via running `poetry run flake8`
- Make sure flake8 is passing for any merge request

### Updating Dependencies
- Use the poetry commands for adding and updating dependencies.
- For general dependency updates it is `poetry update`
- For sphinx to get the new requirements.txt you must run 
  `poetry export -f requirements.txt --output docs/requirements.txt --without-hashes --dev`
  
### Building Documentation
- To build the documentation locally you can run `poetry run make html`
- Then you can inspect what the readthedocs documentation will look like by opening 
  docs/build/html/index.html
