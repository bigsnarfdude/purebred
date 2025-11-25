import unittest
import numpy as np
from purebred.detections import SpectralSignatureDetector

class TestSpectral(unittest.TestCase):
    def test_detection(self):
        # 1. Create synthetic data
        # Class 0: Clean samples (Gaussian blob)
        np.random.seed(42)
        clean_data = np.random.normal(loc=0.0, scale=1.0, size=(100, 50))
        clean_labels = np.zeros(100)
        
        # Class 0: Poisoned samples (shifted mean in one direction)
        # We add a strong signal in the first dimension
        poison_data = np.random.normal(loc=0.0, scale=1.0, size=(10, 50))
        poison_data[:, 0] += 5.0 # Shift mean significantly
        poison_labels = np.zeros(10)
        
        # Combine
        features = np.vstack([clean_data, poison_data])
        labels = np.concatenate([clean_labels, poison_labels])
        
        # Shuffle (optional, but good practice)
        perm = np.random.permutation(len(labels))
        features = features[perm]
        labels = labels[perm]
        
        # Track where the poison went
        poison_indices = np.where(features[:, 0] > 2.5)[0] # Rough check based on shift
        
        # 2. Run detector
        detector = SpectralSignatureDetector(outlier_threshold=1.5)
        detected_indices = detector.detect(features, labels)
        
        # 3. Verify
        # We expect most poisoned samples to be detected
        detected_set = set(detected_indices.keys())
        poison_set = set(poison_indices)
        
        # Calculate recall
        intersection = detected_set.intersection(poison_set)
        recall = len(intersection) / len(poison_set)
        
        print(f"Detected {len(detected_set)} samples. True poison count: {len(poison_set)}")
        print(f"Recall: {recall:.2f}")
        
        self.assertGreater(recall, 0.5, "Should detect at least 50% of poisoned samples")

if __name__ == '__main__':
    unittest.main()
