#!/bin/bash
# Quick test runner script

echo "================================"
echo "Todo App - Test Suite"
echo "================================"
echo ""

# Activate virtual environment
source .venv/bin/activate

echo "📊 Running all tests with coverage..."
echo ""

pytest todos/tests/ \
    --cov=todos \
    --cov-report=html \
    --cov-report=term-missing \
    --verbose

echo ""
echo "================================"
echo "Test Summary"
echo "================================"
echo ""
echo "✅ Coverage HTML Report: htmlcov/index.html"
echo "Run: open htmlcov/index.html"
echo ""
echo "📚 Testing Documentation: TESTING.md"
echo ""
