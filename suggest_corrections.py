import difflib
# from collections import defaultdict

class SuggestCorrections:
    def __init__(self, word_count, ngram_model):
        """
        Initializes the SuggestCorrections class.
        
        Parameters:
        word_count (dict): A dictionary containing the frequency of each word in the training data.
        ngram_model (NGramModel): An instance of the NGramModel class used for contextual scoring.
        """
        self.word_count = word_count  # Dictionary of word frequencies
        self.ngram_model = ngram_model  # N-gram model for contextual scoring

    def get_similar_words(self, word):
        """
        Finds words from the training data that are close matches to the given word.
        
        Parameters:
        word (str): The word for which to find similar words.
        
        Returns:
        list of str: A list of words from the training data that closely match the given word.
        """
        # Use difflib to find words that are close matches
        return difflib.get_close_matches(word, self.word_count.keys())

    def rank_suggestions(self, word, prev_word, next_word):
        """
        Ranks the suggestions for a given word based on frequency and contextual relevance.
        
        Parameters:
        word (str): The word for which to generate suggestions.
        prev_word (str): The word preceding the current word in the text.
        next_word (str): The word following the current word in the text.
        
        Returns:
        list of tuples: Each tuple contains a suggestion and its corresponding score.
        """
        suggestions = self.get_similar_words(word)  # Get potential suggestions
        ranked_suggestions = []
        
        for suggestion in suggestions:
            # Calculate a score based on the word's frequency in the training data
            freq_score = self.word_count.get(suggestion, 0)
            
            # Calculate contextual scores using the N-gram model
            prev_ngram_score = self.ngram_model.predict(prev_word, suggestion)
            next_ngram_score = self.ngram_model.predict(suggestion, next_word)
            
            # Combine the scores to form a total score
            total_score = freq_score + prev_ngram_score + next_ngram_score
            
            # Append the suggestion and its score to the ranked suggestions list
            ranked_suggestions.append((suggestion, total_score))
        
        # Sort the suggestions by total score in descending order
        ranked_suggestions.sort(key=lambda x: x[1], reverse=True)
        return ranked_suggestions

    def suggest(self, word, prev_word, next_word):
        """
        Suggests corrections for a word based on its context.
        
        Parameters:
        word (str): The word to be corrected.
        prev_word (str): The preceding word in the text.
        next_word (str): The following word in the text.
        
        Returns:
        list of tuples: Each tuple contains a suggested correction and its score.
        """
        if word in self.word_count:
            return []  # If the word is in the training data, it's considered correct
        
        ranked_suggestions = self.rank_suggestions(word, prev_word, next_word)
        return ranked_suggestions
