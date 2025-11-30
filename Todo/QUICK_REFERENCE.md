# Quick Reference: Test Commands

## Essential Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
pytest todos/tests/ -v

# Run with coverage report
pytest todos/tests/ --cov=todos --cov-report=term-missing

# Generate HTML coverage
./run_tests.sh

# View HTML coverage in browser
open htmlcov/index.html
```

## Test Selection

```bash
# Run specific file
pytest todos/tests/test_models.py -v

# Run specific test class
pytest todos/tests/test_models.py::TestTodoModel -v

# Run specific test method
pytest todos/tests/test_models.py::TestTodoModel::test_create_todo_basic -v

# Match test by name
pytest todos/tests/ -k "create" -v

# Run with pattern
pytest todos/tests/ -k "model and create" -v
```

## Debugging Options

```bash
# Show print statements
pytest todos/tests/ -s

# Stop on first failure
pytest todos/tests/ -x

# Run last failed tests
pytest todos/tests/ --lf

# Run failed tests first, then others
pytest todos/tests/ --ff

# Show local variables on failure
pytest todos/tests/ -l

# Verbose with full traceback
pytest todos/tests/ -vv --tb=long
```

## Coverage Reports

```bash
# Terminal coverage report
pytest todos/tests/ --cov=todos --cov-report=term-missing

# HTML coverage report
pytest todos/tests/ --cov=todos --cov-report=html

# Multiple formats
pytest todos/tests/ --cov=todos \
  --cov-report=term-missing \
  --cov-report=html \
  --cov-report=xml

# Coverage for specific file
pytest todos/tests/ --cov=todos.models --cov-report=term-missing
```

## Performance

```bash
# Show slowest 10 tests
pytest todos/tests/ --durations=10

# Quiet output (fewer lines)
pytest todos/tests/ -q

# Very quiet (pass/fail only)
pytest todos/tests/ -qq

# Parallel execution (requires pytest-xdist)
pytest todos/tests/ -n auto
```

## Test Statistics

```bash
# Collect tests without running
pytest todos/tests/ --collect-only -q

# Show all test names
pytest todos/tests/ --collect-only

# Show test count
pytest todos/tests/ --collect-only -q | tail -1
```

## Summary

| Task | Command |
|------|---------|
| Run all tests | `pytest todos/tests/ -v` |
| With coverage | `pytest todos/tests/ --cov=todos --cov-report=term-missing` |
| HTML coverage | `./run_tests.sh` |
| Quick tests | `pytest todos/tests/ -q` |
| Debug tests | `pytest todos/tests/ -vv -s` |
| Stop on failure | `pytest todos/tests/ -x` |
| Last failed | `pytest todos/tests/ --lf` |
| Specific file | `pytest todos/tests/test_models.py -v` |
| Pattern match | `pytest todos/tests/ -k "create"` |

## Test Results Indicators

- ✅ PASSED - Test succeeded
- ❌ FAILED - Test failed
- ⏭️ SKIPPED - Test skipped
- ⚠️ XFAIL - Expected failure
- ⚠️ XPASS - Unexpected pass
- ⚠️ ERROR - Error during test

## Coverage Thresholds

- **Excellent:** > 95%
- **Good:** 85-95%
- **Acceptable:** 70-85%
- **Poor:** < 70%

Current: **98% ✅ (Excellent)**

## Files

- **Test Configuration:** `pytest.ini`
- **Test Fixtures:** `todos/tests/conftest.py`
- **Model Tests:** `todos/tests/test_models.py`
- **Form Tests:** `todos/tests/test_forms.py`
- **View Tests:** `todos/tests/test_views.py`
- **Integration Tests:** `todos/tests/test_integration.py`

## Documentation

- `README.md` - Project overview
- `TESTING.md` - Comprehensive guide
- `TEST_SUMMARY.md` - Quick reference
- `TEST_ARCHITECTURE.md` - Technical details
- `TEST_IMPLEMENTATION.md` - Implementation summary

---

**Status:** 70/70 tests passing | 98% coverage | Ready for production ✅
