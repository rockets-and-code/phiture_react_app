# Team Builder API Test Suite

This directory contains comprehensive unit tests for the Team Builder API, covering both the API endpoints (`main.py`) and the core business logic (`logic.py`).

## Test Structure

```
tests/
├── __init__.py                 # Package marker
├── test_logic.py              # Tests for logic functions
├── test_main.py               # Tests for API endpoints
└── README.md                  # This file
```

## Test Coverage

### Logic Tests (`test_logic.py`)

**`TestCalculateRatingToPriceRatio`**
- ✅ Basic calculation verification
- ✅ Data preservation validation  
- ✅ Edge cases (very low/high prices)

**`TestLowestPriceCombination`**
- ✅ Minimum budget calculation with sample data ($245)
- ✅ Error handling for insufficient categories
- ✅ Correct selection of cheapest products per category
- ✅ Multiple products per category handling

**`TestFindBestProductsForCategories`**
- ✅ Product selection within reasonable budgets
- ✅ Tight budget constraint handling
- ✅ Insufficient budget edge cases

**`TestFindBestCombination`**
- ✅ Optimal combination selection
- ✅ Budget sensitivity verification

**`TestCurateProductTeam`** (Main Function)
- ✅ End-to-end team curation with sample data
- ✅ Minimum budget handling
- ✅ Insufficient categories error handling
- ✅ Budget sensitivity (different budgets → different results)
- ✅ Product model conversion validation

### API Tests (`test_main.py`)

**`TestRootEndpoint`**
- ✅ Root endpoint response structure

**`TestHealthEndpoint`**
- ✅ Health check functionality

**`TestTeamBuilderEndpoint`**
- ✅ Valid budget requests
- ✅ Minimum budget acceptance
- ✅ Below-minimum budget rejection (400 error)
- ✅ Negative budget validation (422 error)
- ✅ Zero budget handling
- ✅ Missing/invalid parameters (422 errors)
- ✅ Float budget type validation
- ✅ High budget handling
- ✅ Budget sensitivity verification

**`TestTeamBuilderEndpointAsync`**
- ✅ Direct async function testing
- ✅ Response model validation
- ✅ Exception handling

**`TestTeamBuilderEndpointEdgeCases`**
- ✅ Empty result handling
- ✅ Exception propagation
- ✅ CORS middleware verification

**`TestAPIIntegration`**
- ✅ Complete workflow testing
- ✅ API consistency across multiple calls

## Running Tests

### Run All Tests
```bash
# From backend directory
python3 -m pytest tests/ -v

# Or use the test runner script
python3 run_tests.py
```

### Run Specific Test Categories
```bash
# Run only logic tests
python3 -m pytest tests/test_logic.py -v

# Run only API tests  
python3 -m pytest tests/test_main.py -v

# Run specific test patterns
python3 run_tests.py "budget"        # Tests containing "budget"
python3 run_tests.py "minimum"       # Tests containing "minimum"
```

### Test Output Examples

**Successful Test Run:**
```
============= test session starts =============
platform darwin -- Python 3.8.5, pytest-8.3.5
collected 39 items

tests/test_logic.py::TestCalculateRatingToPriceRatio::test_calculate_rating_to_price_ratio_basic PASSED
tests/test_main.py::TestTeamBuilderEndpoint::test_team_builder_valid_budget PASSED
...
============= 39 passed in 5.76s =============
```

## Test Dependencies

```bash
pip install -r test-requirements.txt
```

Required packages:
- `pytest==8.3.5` - Testing framework
- `pytest-asyncio==0.24.0` - Async test support
- `httpx==0.28.1` - HTTP client for API testing
- `fastapi[test]==0.116.1` - FastAPI test utilities

## Test Configuration

Tests are configured via `pytest.ini`:
- Test files: `test_*.py`
- Test functions: `test_*`
- Async mode: Auto-detection
- Verbose output with short tracebacks

## Key Test Features

1. **Comprehensive Coverage**: Tests cover all public functions and API endpoints
2. **Edge Case Handling**: Invalid inputs, boundary conditions, error scenarios
3. **Budget Sensitivity**: Verifies different budgets produce different results
4. **Data Integrity**: Validates response structures and model conversion
5. **Error Validation**: Proper HTTP status codes and exception handling
6. **Integration Testing**: End-to-end workflow verification

## Test Data

Tests use:
- **Sample data**: From `constants.py` for realistic scenarios
- **Mock data**: Custom test data for edge cases
- **Mocking**: `unittest.mock` for isolating components

## Continuous Integration

These tests are designed to run in CI/CD pipelines:
- No external dependencies
- Deterministic results
- Fast execution (~6 seconds)
- Clear pass/fail criteria
