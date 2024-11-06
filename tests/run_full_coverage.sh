#!/bin/bash

# Run the full test suite
coverage run -m pytest

# Generate screenshots (only need to run for one locale to assess coverage)
coverage run -m pytest tests/screenshot_generator/generator.py --locale es

# Combine the above coverage results; also cleans up any prior .coverage.* results files
coverage combine

# Show the cli report
coverage report

# Generate the interactive html report
coverage html
