#!/usr/bin/env python3
"""
Test runner script for the Team Builder API

This script runs all unit tests and provides coverage information.
"""

import subprocess
import sys
import os


def run_tests():
    """Run all unit tests"""
    print("🧪 Running Team Builder API Tests...")
    print("=" * 60)
    
    # Change to backend directory if not already there
    if not os.path.exists("tests"):
        os.chdir("backend")
    
    try:
        # Run pytest with verbose output
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v", 
            "--tb=short",
            "--color=yes"
        ], check=False)
        
        if result.returncode == 0:
            print("\n✅ All tests passed!")
            print("=" * 60)
            return True
        else:
            print(f"\n❌ Some tests failed (exit code: {result.returncode})")
            print("=" * 60)
            return False
            
    except FileNotFoundError:
        print("❌ pytest not found. Please install test dependencies:")
        print("   pip install -r test-requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def run_specific_tests(pattern):
    """Run tests matching a specific pattern"""
    print(f"🧪 Running tests matching: {pattern}")
    print("=" * 60)
    
    if not os.path.exists("tests"):
        os.chdir("backend")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/",
            "-k", pattern,
            "-v", 
            "--tb=short",
            "--color=yes"
        ], check=False)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def main():
    """Main function"""
    if len(sys.argv) > 1:
        # Run specific tests
        pattern = sys.argv[1]
        success = run_specific_tests(pattern)
    else:
        # Run all tests
        success = run_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
