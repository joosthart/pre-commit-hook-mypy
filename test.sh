#!/bin/bash
set -e

# Install the hook in development mode
python3 -m pip install -e .

# Create an initial commit if it doesn't exist
if ! git rev-parse HEAD >/dev/null 2>&1; then
  echo "Creating initial commit..."
  git config --local user.email "test@example.com"
  git config --local user.name "Test User"
  git add README.md
  git commit -m "Initial commit"
fi

# Display the direct mypy output for comparison
echo "====================== RUNNING DIRECT MYPY ======================"
python3 -m mypy test_example/good_file.py test_example/bad_file.py || true
echo ""

# Test filtering functionality
echo "====================== RUNNING MYPY-COMMITTED ON ALL FILES ======================"
python3 mypy_committed.py --show-all-errors test_example/good_file.py test_example/bad_file.py || true
echo ""

echo "====================== FILTERING ONLY GOOD FILE ======================"
python3 mypy_committed.py test_example/good_file.py
echo ""

echo "====================== FILTERING ONLY BAD FILE ======================"
python3 mypy_committed.py test_example/bad_file.py || true
echo ""

# Test with git staging
echo "====================== TESTING WITH GIT STAGING ======================"
git add test_example/good_file.py
python3 mypy_committed.py test_example/good_file.py test_example/bad_file.py || true
echo ""

git add test_example/bad_file.py
python3 mypy_committed.py test_example/good_file.py test_example/bad_file.py || true
echo ""

# Clean up
git reset HEAD test_example/good_file.py test_example/bad_file.py

echo "Done testing!" 