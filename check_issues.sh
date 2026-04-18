#!/bin/bash

echo "=== Searching for remaining shell arithmetic operations ==="
grep -r '\$((.*))' .github/workflows/ || echo "No shell arithmetic found"

echo ""
echo "=== Searching for remaining GitHub Copilot actions ==="
grep -r 'github/copilot' .github/workflows/ || echo "No GitHub Copilot actions found"

echo ""
echo "=== Searching for remaining shell arithmetic patterns ==="
grep -r '\$(' .github/workflows/ | grep -E '(count|total).*=' || echo "No problematic patterns found"

echo ""
echo "=== Checking for any uses: statements with copilot ==="
grep -r 'uses:.*copilot' .github/workflows/ || echo "No copilot uses statements found"