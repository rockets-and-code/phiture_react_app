# Team Builder API - Testing Setup Guide

This guide provides step-by-step instructions for setting up and running unit tests in a clean virtual environment.

## 🎯 Quick Start

```bash
# Navigate to backend directory
cd /Users/marianita/phiture_react_app/backend

# Create and activate virtual environment
python3 -m venv test-env
source test-env/bin/activate

# Install dependencies and run tests
pip install -r requirements.txt -r test-requirements.txt
python3 run_tests.py

# Deactivate when done
deactivate
```

## 📋 Detailed Setup Instructions

### Step 1: Navigate to Backend Directory
```bash
cd /Users/marianita/phiture_react_app/backend
pwd  # Should show: /Users/marianita/phiture_react_app/backend
```

### Step 2: Create Virtual Environment
```bash
# Create a new virtual environment named 'test-env'
python3 -m venv test-env
```

### Step 3: Activate Virtual Environment

**On macOS/Linux:**
```bash
source test-env/bin/activate
```

**On Windows:**
```cmd
test-env\Scripts\activate
```

**You'll know it's activated when you see:**
```bash
(test-env) user@computer:/path/to/backend$
```

### Step 4: Install Dependencies
```bash
# Install main application dependencies
pip install -r requirements.txt

# Install test dependencies
pip install -r test-requirements.txt

# Or install everything at once
pip install -r requirements.txt -r test-requirements.txt
```

### Step 5: Verify Installation
```bash
# Check that pytest is installed
python3 -m pytest --version

# Check that all packages are installed
pip list
```

### Step 6: Run Tests
```bash
# Run all tests (recommended)
python3 run_tests.py

# Or use pytest directly
python3 -m pytest tests/ -v
```

### Step 7: Deactivate When Done
```bash
# Deactivate the virtual environment
deactivate
```

## 🔄 Daily Testing Workflow

### First Time Setup
```bash
cd /Users/marianita/phiture_react_app/backend
python3 -m venv test-env
source test-env/bin/activate
pip install -r requirements.txt -r test-requirements.txt
```

### Regular Testing Sessions
```bash
# Activate environment
cd /Users/marianita/phiture_react_app/backend
source test-env/bin/activate

# Run tests
python3 run_tests.py

# Deactivate when done
deactivate
```

## 📁 File Structure Overview

```
/Users/marianita/phiture_react_app/backend/
├── test-env/                      # Virtual environment (created by you)
│   ├── bin/activate              # Activation script
│   ├── lib/python3.x/            # Installed packages
│   └── ...
├── tests/                        # Test files
│   ├── test_logic.py            # Logic function tests
│   ├── test_main.py             # API endpoint tests
│   └── README.md                # Test documentation
├── requirements.txt              # Main app dependencies
├── test-requirements.txt         # Test-specific dependencies
├── run_tests.py                  # Custom test runner
├── pytest.ini                   # Test configuration
├── main.py                       # API endpoints
├── logic.py                      # Business logic
└── README_TESTING.md             # This file
```

## 📦 Dependencies Breakdown

### Main Dependencies (`requirements.txt`)
```
fastapi==0.116.1
uvicorn==0.33.0
pydantic==2.10.6
```

### Test Dependencies (`test-requirements.txt`)
```
pytest==8.3.5
pytest-asyncio==0.24.0
httpx==0.28.1
fastapi[test]==0.116.1
```

## 🧪 Test Execution Options

### Basic Test Commands
```bash
# Activate environment first
source test-env/bin/activate

# Run all tests (39 tests)
python3 run_tests.py

# Run with pytest directly
python3 -m pytest tests/ -v

# Run specific test files
python3 -m pytest tests/test_logic.py -v      # Logic tests only
python3 -m pytest tests/test_main.py -v       # API tests only
```

### Pattern-Based Testing
```bash
# Budget-related tests
python3 run_tests.py "budget"

# Minimum budget tests
python3 run_tests.py "minimum"

# Exception handling tests
python3 run_tests.py "exception"

# Team builder endpoint tests
python3 run_tests.py "team_builder"
```

### Advanced Testing Options
```bash
# Stop at first failure
python3 -m pytest tests/ -x

# Show slowest tests
python3 -m pytest tests/ --durations=10

# Quiet mode
python3 -m pytest tests/ -q

# Very verbose
python3 -m pytest tests/ -vv

# Run specific test
python3 -m pytest tests/test_logic.py::TestCurateProductTeam::test_curate_product_team_with_sample_data -v
```


## 🛠️ Troubleshooting

### Virtual Environment Issues

**Problem: `command not found: python3`**
```bash
# Try using python instead of python3
python -m venv test-env

# Or check your Python installation
which python
which python3
```

**Problem: Virtual environment not activating**
```bash
# Make sure you're in the right directory
pwd

# Try absolute path
source /Users/marianita/phiture_react_app/backend/test-env/bin/activate

# Check if the activate script exists
ls -la test-env/bin/activate
```

**Problem: `pip: command not found`**
```bash
# Use python -m pip instead
python3 -m pip install -r requirements.txt
```
