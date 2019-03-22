SHELL := /bin/bash

.PHONY: help format lint tests tests_cov_html test_student test_instructor test_core debug_instructor debug_student production_instructor production_student

help:
	@echo "Makefile targets:"
	@echo "    help                  - Display this message"
	@echo "    format                - Auto reformat code"
	@echo "    tests                 - Run all tests"
	@echo "    tests_cov_html        - Run all tests and report test coverage to the htmlcov directory"
	@echo "    test_core             - Run tests for core"
	@echo "    test_instructor       - Run tests for instructor service"
	@echo "    test_student          - Run tests for student service"
	@echo "    debug_instructor      - Run a local development server for instructor service"
	@echo "    debug_student         - Run a local development server for student service"
	@echo "    production_instructor - Run instructor service in production"
	@echo "    production_student    - Run student service in production"

format: ; black . --exclude venv

lint:
	flake8
	black --check . --exclude venv

tests:
	pytest student_service instructor_service core \
	--cov=core --cov=student_service --cov=instructor_service

tests_cov_html:
	pytest student_service instructor_service core \
	--cov-report html --cov=core --cov=student_service --cov=instructor_service

htmlcov: tests_cov_html

test_student: ; pytest student_service/tests --cov=student_service

test_instructor: ; pytest instructor_service/tests --cov=instructor_service

test_core: ; pytest core/tests --cov=core

debug_instructor: ; python instructor_service/run.py

debug_student: ; python student_service/run.py

