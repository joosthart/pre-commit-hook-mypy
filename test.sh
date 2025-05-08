#!/bin/bash
set -e

# Install the hook in development mode
python3 -m pip install -e .

# Create an initial commit if it doesn't exist
if ! git rev-parse HEAD >/dev/null 2>&1; then
  echo "Creating initial commit..."
  git config --local user.email "hartjoost@gmail.com"
  git config --local user.name "Joost Hart"
  git add README.md
  git commit -m "Initial commit"
fi

# Display the direct mypy output for comparison
echo "====================== RUNNING DIRECT MYPY ======================"
python3 -m mypy test_example/good_file.py test_example/bad_file.py || true
echo ""

# Test filtering functionality
echo "====================== RUNNING MYPY-COMMITTED MANUALLY ======================"
echo "Running with all files (should show errors):"
python3 mypy_committed.py --show-all-errors test_example/good_file.py test_example/bad_file.py || true
echo ""

echo "====================== TESTING WITH GIT STAGING ======================"
# Create a temporary directory for testing with git
TEMP_DIR=$(mktemp -d)
echo "Created temp directory: $TEMP_DIR"
pushd $TEMP_DIR

# Initialize a git repository
git init
git config --local user.email "hartjoost@gmail.com"
git config --local user.name "Joost Hart"

# Create a pre-commit config
cat > .pre-commit-config.yaml << EOF
repos:
-   repo: $(pwd)/..
    rev: main
    hooks:
    -   id: mypy-committed
        verbose: true
EOF

# Install pre-commit
pre-commit install

# Test with a good file (should pass)
cp ../test_example/good_file.py good.py
git add good.py .pre-commit-config.yaml
git commit -m "Add good file"

# Test with a bad file (should fail)
cp ../test_example/bad_file.py bad.py
git add bad.py

# Print debug info
echo "=== Files staged for commit ==="
git diff --cached --name-only

echo "=== Running mypy directly on bad.py ==="
python3 -m mypy bad.py || true

echo "=== Running the pre-commit hook ==="
if git commit -m "Add bad file"; then
  echo "ERROR: Hook should have failed but didn't!"
  exit 1
else
  echo "SUCCESS: Hook failed as expected."
fi

# Clean up
popd
rm -rf $TEMP_DIR

echo "Done testing!" 