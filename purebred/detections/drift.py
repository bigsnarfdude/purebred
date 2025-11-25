import numpy as np
from scipy.stats import ks_2samp
from typing import Dict, List, Tuple, Optional

class DriftDetector:
    """
    Implements a simple feature-wise drift detector using the Kolmogorov-Smirnov (KS) test.
    Detects if the distribution of any feature in the new data has significantly 
    diverged from the reference data.
    """
    def __init__(self, p_value_threshold: float = 0.05, correction: str = "bonferroni"):
        """
        Args:
            p_value_threshold: Significance level for the test.
            correction: Multiple hypothesis testing correction ('bonferroni' or None).
        """
        self.p_value_threshold = p_value_threshold
        self.correction = correction
        self.reference_data: Optional[np.ndarray] = None

    def fit(self, reference_data: np.ndarray):
        """
        Stores the reference data for comparison.
        
        Args:
            reference_data: (N, D) numpy array of reference samples.
        """
        self.reference_data = reference_data

    def predict(self, new_data: np.ndarray) -> Dict[str, any]:
        """
        Checks for drift in the new data compared to reference data.
        
        Args:
            new_data: (M, D) numpy array of new samples.
            
        Returns:
            Dictionary containing:
                - 'is_drift': bool, True if drift detected in ANY feature.
                - 'drift_features': List[int], indices of features that drifted.
                - 'p_values': List[float], p-values for each feature.
        """
        if self.reference_data is None:
            raise ValueError("Detector must be fit with reference data first.")
            
        if self.reference_data.shape[1] != new_data.shape[1]:
            raise ValueError("Feature dimension mismatch.")
            
        n_features = self.reference_data.shape[1]
        p_values = []
        drift_features = []
        
        # Apply correction to threshold
        threshold = self.p_value_threshold
        if self.correction == "bonferroni":
            threshold /= n_features
            
        for i in range(n_features):
            ref_feature = self.reference_data[:, i]
            new_feature = new_data[:, i]
            
            # KS Test
            stat, p_val = ks_2samp(ref_feature, new_feature)
            p_values.append(p_val)
            
            if p_val < threshold:
                drift_features.append(i)
                
        return {
            "is_drift": len(drift_features) > 0,
            "drift_features": drift_features,
            "p_values": p_values,
            "threshold": threshold
        }
