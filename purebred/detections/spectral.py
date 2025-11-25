import numpy as np
from sklearn.decomposition import TruncatedSVD
from typing import Tuple, List, Dict

class SpectralSignatureDetector:
    """
    Implements Spectral Signature Analysis for detecting poisoned samples.
    Based on Tran et al., "Spectral Signatures in Backdoor Attacks" (NeurIPS 2018).
    
    The core idea is that poisoned samples often leave a detectable trace in the 
    spectrum of the covariance matrix of the feature representations.
    """
    def __init__(self, outlier_threshold: float = 1.5):
        """
        Args:
            outlier_threshold: Number of standard deviations to consider an outlier.
                               Tran et al. suggest 1.5 * MAD (Median Absolute Deviation).
        """
        self.outlier_threshold = outlier_threshold

    def detect(self, features: np.ndarray, labels: np.ndarray) -> Dict[int, float]:
        """
        Detects potential poisoned samples.
        
        Args:
            features: (N, D) numpy array of feature representations (e.g., from a penultimate layer).
            labels: (N,) numpy array of class labels.
            
        Returns:
            Dictionary mapping {index: outlier_score} for suspected poisoned samples.
            Higher score = more likely to be poisoned.
        """
        poisoned_indices = {}
        unique_labels = np.unique(labels)
        
        for label in unique_labels:
            # Get indices for this class
            indices = np.where(labels == label)[0]
            if len(indices) < 10:
                continue # Skip classes with too few samples
                
            class_features = features[indices]
            
            # 1. Center the data (mean subtraction)
            mean_feature = np.mean(class_features, axis=0)
            centered_features = class_features - mean_feature
            
            # 2. Compute the top right singular vector (u) of the centered features
            # We use TruncatedSVD for efficiency
            svd = TruncatedSVD(n_components=1, random_state=42)
            svd.fit(centered_features)
            top_eigenvector = svd.components_[0] # Shape (D,)
            
            # 3. Project all samples onto this top eigenvector
            # Scores = (X - mu) * u
            outlier_scores = np.dot(centered_features, top_eigenvector)
            outlier_scores = np.abs(outlier_scores) # We care about magnitude
            
            # 4. Detect outliers based on scores
            # Using simple Z-score here for simplicity, but robust stats (MAD) are better
            # scores_median = np.median(outlier_scores)
            # scores_mad = np.median(np.abs(outlier_scores - scores_median))
            # modified_z_scores = 0.6745 * (outlier_scores - scores_median) / scores_mad
            
            # Let's stick to a simple mean/std for the prototype
            score_mean = np.mean(outlier_scores)
            score_std = np.std(outlier_scores)
            
            threshold = score_mean + (self.outlier_threshold * score_std)
            
            for i, score in enumerate(outlier_scores):
                if score > threshold:
                    original_idx = indices[i]
                    poisoned_indices[original_idx] = float(score)
                    
        return poisoned_indices
