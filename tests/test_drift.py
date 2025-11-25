import unittest
import numpy as np
from purebred.detections import DriftDetector

class TestDrift(unittest.TestCase):
    def test_drift_detection(self):
        np.random.seed(42)
        
        # Reference data: 1000 samples, 5 features, standard normal
        reference_data = np.random.normal(0, 1, (1000, 5))
        
        # Test data 1: No drift (same distribution)
        test_data_no_drift = np.random.normal(0, 1, (500, 5))
        
        # Test data 2: Drift in feature 0 (shifted mean)
        test_data_drift = np.random.normal(0, 1, (500, 5))
        test_data_drift[:, 0] += 1.0 # Significant shift
        
        detector = DriftDetector(p_value_threshold=0.01)
        detector.fit(reference_data)
        
        # Check no drift
        result_no_drift = detector.predict(test_data_no_drift)
        self.assertFalse(result_no_drift["is_drift"])
        self.assertEqual(len(result_no_drift["drift_features"]), 0)
        
        # Check drift
        result_drift = detector.predict(test_data_drift)
        self.assertTrue(result_drift["is_drift"])
        self.assertIn(0, result_drift["drift_features"])
        # Ensure other features didn't trigger false positives (mostly)
        # With random seed 42, others should be fine
        self.assertEqual(len(result_drift["drift_features"]), 1)

if __name__ == '__main__':
    unittest.main()
