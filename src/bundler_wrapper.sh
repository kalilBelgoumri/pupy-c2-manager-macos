#!/bin/bash
# Wrapper script to run deployment_orchestrator.py with proper environment

# Activate the venv
source /Users/kalilbelgoumri/Desktop/pupy_env/bin/activate

# Run the script
python "$@"
