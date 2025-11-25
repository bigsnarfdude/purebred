import secrets
import string
import random
from typing import List, Optional, Tuple

class CanaryGenerator:
    """
    Generates high-entropy canary tokens that are unlikely to appear naturally 
    in a dataset. These serve as 'radioactive' markers.
    """
    def __init__(self, length: int = 16, prefix: str = "PUREBRED_CANARY_"):
        self.length = length
        self.prefix = prefix
        self.alphabet = string.ascii_letters + string.digits

    def generate(self) -> str:
        """Generates a single unique canary token."""
        random_part = ''.join(secrets.choice(self.alphabet) for _ in range(self.length))
        return f"{self.prefix}{random_part}"

    def generate_batch(self, count: int) -> List[str]:
        """Generates a batch of unique canary tokens."""
        return [self.generate() for _ in range(count)]


class CanaryInjector:
    """
    Injects canary tokens into a text dataset.
    """
    def __init__(self, canaries: List[str], strategy: str = "random_insert"):
        """
        Args:
            canaries: List of canary tokens to inject.
            strategy: Injection strategy (currently only 'random_insert' is supported).
        """
        self.canaries = canaries
        self.strategy = strategy

    def inject(self, text: str, canary: Optional[str] = None) -> str:
        """
        Injects a canary into a single text string.
        
        Args:
            text: The original text.
            canary: Specific canary to inject. If None, picks one at random.
            
        Returns:
            The text with the canary injected.
        """
        if not self.canaries and canary is None:
            raise ValueError("No canaries available for injection")
            
        token_to_inject = canary if canary else random.choice(self.canaries)
        
        if self.strategy == "random_insert":
            # Simple whitespace insertion
            words = text.split()
            if not words:
                return f"{text} {token_to_inject}"
                
            insert_pos = random.randint(0, len(words))
            words.insert(insert_pos, token_to_inject)
            return " ".join(words)
        
        return text

    def inject_dataset(self, dataset: List[str], injection_rate: float = 0.1) -> Tuple[List[str], List[str]]:
        """
        Injects canaries into a list of strings (dataset).
        
        Args:
            dataset: List of text samples.
            injection_rate: Probability (0.0 to 1.0) of injecting a canary into a sample.
            
        Returns:
            Tuple of (modified_dataset, injected_samples_indices)
        """
        modified_dataset = []
        injected_indices = []
        
        for i, text in enumerate(dataset):
            if random.random() < injection_rate:
                modified_dataset.append(self.inject(text))
                injected_indices.append(i)
            else:
                modified_dataset.append(text)
                
        return modified_dataset, injected_indices
