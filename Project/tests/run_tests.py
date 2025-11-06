#!/usr/bin/env python3
"""
Test runner for the OOP order system project.
This script discovers and runs all tests in the test directory.
"""

import unittest
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def run_all_tests():
    """Discover and run all tests in the test directory"""
    # Discover all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return the result
    return result.wasSuccessful()


def run_specific_test(test_module):
    """Run a specific test module"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_module)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Run a specific test module
        test_module = sys.argv[1]
        print(f"Running tests for module: {test_module}")
        success = run_specific_test(test_module)
    else:
        # Run all tests
        print("Running all tests...")
        success = run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)