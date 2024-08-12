class NGramModel:
    def __init__(self, n=2):
        """
        Initializes the NGramModel with the specified n-gram size.
        
        Parameters:
        n (int): The size of the n-grams (e.g., 2 for bigrams, 3 for trigrams).
        """
        self.n = n  # Set the size of n-grams
        self.ngrams = {}  # Dictionary to store the frequency of each n-gram

    def train(self, sentences):
        """
        Trains the N-gram model using the provided sentences.
        
        Parameters:
        sentences (list of list of str): List of tokenized sentences to train on.
        
        Process:
        - Adds <START> and <END> tokens to handle the beginning and end of sentences.
        - Generates n-grams from the sentences and counts their frequencies.
        """
        for sentence in sentences:
            # Add <START> and <END> tokens to handle sentence boundaries
            tokens = ["<START>"] + sentence + ["<END>"]
            
            # Generate n-grams and count their frequencies
            for i in range(len(tokens) - self.n + 1):
                ngram = tuple(tokens[i:i + self.n])  # Extract n-gram tuple
                # Update the frequency count for the n-gram
                self.ngrams[ngram] = self.ngrams.get(ngram, 0) + 1

    def predict(self, prev, word):
        """
        Predicts the frequency of an n-gram based on the previous word and the current word.
        
        Parameters:
        prev (str): The previous word in the context.
        word (str): The current word in the context.
        
        Returns:
        int: The frequency count of the n-gram (prev, word) from the training data.
        """
        ngram = (prev, word)  # Create n-gram tuple from previous and current word
        return self.ngrams.get(ngram, 0)  # Return the frequency count, default to 0 if n-gram not found
