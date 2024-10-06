# Add sh to your path as described here https://github.com/casey/just/blob/master/README.md#prerequisites
# The sh shell is probably a much easier solution compatibility-wise
set windows-shell := ["sh.exe", "-c"]
VENV := justfile_directory() + '/.venv'
VENV_BIN := justfile_directory() + if os() == "windows" {'/.venv/Scripts'} else {'/.venv/bin'}
BUILD_DIR := justfile_directory() + '/build'
PYTHON := if os() == "windows" { "py" } else { "python3" }
EXPECTED_PYTHON_VERSION := "3.11"
CURRENT_PYTHON_VERSION := if os() == "windows" { `py --version` } else { `python3 --version` }
PYTHON_VALIDATION_REGEX := EXPECTED_PYTHON_VERSION + '.+'
IS_CORRECT_PYTHON_VERSION := if CURRENT_PYTHON_VERSION =~ PYTHON_VALIDATION_REGEX {"true"} else {"false"}
IMAGE_NAME := "mqtt-to-bigquery"
LOCAL_TAG := "latest"

@default:
  just --list

@_check_python_version:
  echo {{ if IS_CORRECT_PYTHON_VERSION == "true" { "Initializing.." } else { "Incorrect Python version " + CURRENT_PYTHON_VERSION + "! Expected: " + EXPECTED_PYTHON_VERSION } }}
  echo {{ if IS_CORRECT_PYTHON_VERSION == "true" {""} else {error("")} }}

@init: _check_python_version
  just install

initenv:
  @echo 'Creating virtual environment!'
  @{{PYTHON}} -m venv "{{VENV}}"

install: initenv
  "{{VENV_BIN}}/pip" install -r "./requirements.txt"

@test:
  "{{VENV_BIN}}/pytest" .
  echo "tests: OK ✅"

@clean:
  echo "Removing virtual environment..."
  rm -rf "{{VENV}}"
  echo "Removing build directory..."
  rm -rf "{{BUILD_DIR}}"
  echo "Environment cleaned ✅"

@build:
  docker build . -t {{IMAGE_NAME}}:{{LOCAL_TAG}} --platform linux/amd64

@save:
  mkdir -p {{BUILD_DIR}}
  tar -cvf {{BUILD_DIR}}/{{IMAGE_NAME}}.tar Dockerfile main.py requirements.txt service_account.json

@run:
   {{VENV_BIN}}/python main.py

@docker_run:
  docker run -d \
    --name mqtt-to-bigquery \
    --user root:root \
    mqtt-to-bigquery:latest

# docker run -d \
#   --name mqtt-to-bigquery \
#   --restart unless-stopped \
#   -v ~/bigquery:/app/etc:ro \
#   --user root:root \
#   mqtt-to-bigquery:latest