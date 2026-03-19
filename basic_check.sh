#!/bin/bash
cd /workspace
echo "Current directory: $(pwd)"
echo "Python version: $(python3 --version)"
echo "Files in workspace:"
ls -la
echo
echo "Testing basic Python import:"
python3 simple_test.py