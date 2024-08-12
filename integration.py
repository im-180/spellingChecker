from data_collector import DataCollector
from text_preprocessor import TextPreprocessor
from feature_engineering import FeatureExtractor
from model import SpellCheckerModelTrainer
from context_analysis import NGramModel
from suggest_corrections import SuggestCorrections

from collections import defaultdict


class SpellChecker:
    def __init__(self):
        """
        Initializes the SpellChecker class with instances of the required components.
        """
        self.data_collector = DataCollector()  # Data collector for gathering training data
        self.text_preprocessor = TextPreprocessor()  # Text preprocessor for tokenizing and cleaning text
        self.feature_extractor = FeatureExtractor()  # Feature extractor for creating features from data (not used in this example)
        self.model_trainer = SpellCheckerModelTrainer()  # Model trainer for training the spell checker model
        self.ngram_model = None  # Placeholder for the N-gram model, to be initialized later
        self.suggest_corrections = None  # Placeholder for the suggestion corrections model, to be initialized later

    def train(self, correct_data_file):
        """
        Trains the spell checker and context models using the provided data file.
        
        Parameters:
        correct_data_file (str): Path to the file containing correct sentences for training.
        """
        # Collect and preprocess training data
        self.data_collector.collect_data(correct_data_file)
        preprocessed_data = self.text_preprocessor.preprocess(self.data_collector.get_correct_sentences())
        
        # Train the spell checker model
        self.model_trainer.train(preprocessed_data)
        
        # Initialize and train the N-gram model with bigrams
        self.ngram_model = NGramModel(n=2)  # Example with bigrams
        self.ngram_model.train(preprocessed_data)
        
        # Initialize SuggestCorrections with trained models
        self.suggest_corrections = SuggestCorrections(
            word_count=self.model_trainer.word_count,
            ngram_model=self.ngram_model
        )
        print("Congratulations! 🎉 Training complete. The ML model and N-gram model are ready!.")

    def check(self, text):
        """
        Checks the provided text for spelling and contextual errors.
        
        Parameters:
        text (str): The text to be checked.
        
        Returns:
        list of tuples: Each tuple contains a token and a description of the detected issue.
        """
        # Tokenize the input text
        tokens = self.text_preprocessor.tokenize(text)
        corrections = []  # List to hold detected errors
        suggestions = {}  # Dictionary to hold suggestions for misspelled words
        token_counts = defaultdict(int)  # To count occurrences of each token
        token_indices = defaultdict(list)  # To track indices of each token

        # Count token occurrences and store indices
        for i, token in enumerate(tokens):
            token_counts[token] += 1
            token_indices[token].append(i)
        
        # Check for repeated words
        for token, count in token_counts.items():
            if count > 1 and token not in self.model_trainer.word_count:
                corrections.append((token, "Repeated word detected"))

        # Check each token for spelling and contextual issues
        for i, token in enumerate(tokens):
            prev_word = tokens[i - 1] if i > 0 else "<START>"  # Word before the current token
            next_word = tokens[i + 1] if i < len(tokens) - 1 else "<END>"  # Word after the current token

            # Check for spelling issues using the spell checker model
            if token not in self.model_trainer.word_count:
                if not self.model_trainer.predict(token, prev_word, next_word):
                    if self.suggest_corrections:
                        # Suggest corrections for misspelled words
                        suggestion_list = self.suggest_corrections.suggest(token, prev_word, next_word)
                        suggestions[token] = suggestion_list
                    corrections.append((token, "Misspelling"))

            # Check context using the N-gram model
            if self.ngram_model:
                prev_ngram_score = self.ngram_model.predict(prev_word, token)
                next_ngram_score = self.ngram_model.predict(token, next_word)
                
                if prev_ngram_score == 0 and next_ngram_score == 0:
                    corrections.append((token, "Contextual Error->Check the previous or the next word"))
                    
            # Check if the next word fits the context based on the training data
            if i < len(tokens) - 1:
                next_token = tokens[i + 1]
                if not self.ngram_model or not self.ngram_model.predict(token, next_token):
                    corrections.append((next_token, "Contextual Mismatch"))

        # Include suggestions in the corrections if any exist
        if suggestions:
            corrections.append(("Suggestions", suggestions))

        return corrections
