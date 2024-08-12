class FeatureExtractor:
    def generate_word_frequency(self, preprocessed_data):
        """
        Generates a frequency count of each word in the preprocessed data.

        :param preprocessed_data: A list of lists, where each inner list represents a tokenized sentence.
        :return: A dictionary where keys are words and values are their respective frequencies.
        """
        # Initialize an empty dictionary to hold word frequencies.
        word_frequency = {}
        # Iterate over each list of tokens (each sentence) in the preprocessed data.
        for tokens in preprocessed_data:
            # Iterate over each token in the current list of tokens.
            for token in tokens:
                # Update the frequency count for the token. If the token is not in the dictionary, initialize its count to 0.
                word_frequency[token] = word_frequency.get(token, 0) + 1
        # Return the dictionary containing word frequencies.
        return word_frequency

    def extract_features(self, sentence, index):
        """
        Extracts the word, previous word, and next word features from a sentence at a given index.

        :param sentence: A list of words representing a tokenized sentence.
        :param index: The position of the word in the sentence for which features are to be extracted.
        :return: A tuple containing the word at the specified index, the previous word, and the next word.
        """
        # Get the word at the specified index in the sentence.
        word = sentence[index]
        # Determine the previous word. If the index is 0 (the start of the sentence), use "<START>" as a placeholder.
        prev_word = sentence[index - 1] if index > 0 else "<START>"
        # Determine the next word. If the index is the last word in the sentence, use "<END>" as a placeholder.
        next_word = sentence[index + 1] if index < len(sentence) - 1 else "<END>"
        # Return a tuple containing the word, previous word, and next word.
        return word, prev_word, next_word
