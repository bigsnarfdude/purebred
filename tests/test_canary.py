import unittest
from purebred.detections import CanaryGenerator, CanaryInjector

class TestCanary(unittest.TestCase):
    def test_generator(self):
        generator = CanaryGenerator(length=10, prefix="TEST_")
        canary = generator.generate()
        self.assertTrue(canary.startswith("TEST_"))
        self.assertEqual(len(canary), 15) # 5 for prefix + 10 random
        
        batch = generator.generate_batch(100)
        self.assertEqual(len(set(batch)), 100) # Ensure uniqueness

    def test_injector(self):
        canaries = ["CANARY_1", "CANARY_2"]
        injector = CanaryInjector(canaries)
        
        text = "Hello world"
        injected = injector.inject(text, canary="CANARY_1")
        self.assertIn("CANARY_1", injected)
        
        dataset = ["Sample 1", "Sample 2", "Sample 3", "Sample 4", "Sample 5"] * 20 # 100 samples
        modified, indices = injector.inject_dataset(dataset, injection_rate=0.5)
        
        # Check that we injected roughly 50%
        self.assertTrue(30 < len(indices) < 70)
        
        # Check that modified samples actually contain canaries
        for idx in indices:
            self.assertTrue(any(c in modified[idx] for c in canaries))

if __name__ == '__main__':
    unittest.main()
