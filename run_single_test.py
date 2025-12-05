# -*- coding: utf-8 -*-
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the specific test
if __name__ == "__main__":
    import unittest
    from TestScripts.test_feature_12_submit_product_returns import TestFeature12SubmitProductReturns
    
    # Create a test suite
    suite = unittest.TestSuite()
    suite.addTest(TestFeature12SubmitProductReturns('test_tc012_02_return_submit_error'))
    
    # Run the test
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    # Print failures
    if result.failures:
        print("\n" + "="*60)
        print("FAILURES:")
        print("="*60)
        for test, traceback in result.failures:
            print(f"\n{test}:")
            print(traceback)
    
    # Print errors
    if result.errors:
        print("\n" + "="*60)
        print("ERRORS:")
        print("="*60)
        for test, traceback in result.errors:
            print(f"\n{test}:")
            print(traceback)
    
    sys.exit(0 if result.wasSuccessful() else 1)
