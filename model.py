from collections import defaultdict #reduces the amount of boilerplate code


class SpellCheckerModelTrainer:
    def __init__(self):
        """
        Initializes the SpellCheckerModelTrainer class.

        - `word_context`: A defaultdict of dictionaries to store context information. 
          Each word maps to a dictionary containing 'prev' and 'next' word frequencies.
        - `word_count`: A defaultdict to store the frequency count of each word.
        """
        # Default dictionary to store previous and next word frequencies for each word.
        self.word_context = defaultdict(lambda: {"prev": defaultdict(int), "next": defaultdict(int)})
        # Default dictionary to store the frequency count of each word.
        self.word_count = defaultdict(int)

    def train(self, sentences):
        """
        Trains the model using a list of tokenized sentences.

        :param sentences: A list of lists, where each inner list represents a tokenized sentence.
        """
        # Iterate over each sentence in the list of sentences.
        for sentence in sentences:
            # Iterate over each word in the current sentence, using its index.
            for i, word in enumerate(sentence):
                # Increment the count of the current word.
                self.word_count[word] += 1
                
                # Determine the previous word, using "<START>" if the current word is at the start.
                prev_word = sentence[i - 1] if i > 0 else "<START>"
                # Determine the next word, using "<END>" if the current word is at the end.
                next_word = sentence[i + 1] if i < len(sentence) - 1 else "<END>"
                
                # Increment the frequency count of the previous word for the current word.
                self.word_context[word]["prev"][prev_word] += 1
                # Increment the frequency count of the next word for the current word.
                self.word_context[word]["next"][next_word] += 1

    def predict(self, word, prev_word, next_word):
        """
        Predicts whether the word is used correctly based on its context.

        :param word: The word to check.
        :param prev_word: The previous word in the context.
        :param next_word: The next word in the context.
        :return: True if the word is likely used correctly based on its context; False otherwise.
        """
        # If the word is not in the word count dictionary, return False.
        if word not in self.word_count:
            return False

        # Calculate the probability of the previous word given the current word.
        prev_prob = (self.word_context[word]["prev"].get(prev_word, 0) + 1) / (self.word_count[word] + len(self.word_context))
        # Calculate the probability of the next word given the current word.
        next_prob = (self.word_context[word]["next"].get(next_word, 0) + 1) / (self.word_count[word] + len(self.word_context))
        
        # Return True if both probabilities are greater than 0.01; otherwise, return False.
        return prev_prob > 0.01 and next_prob > 0.01
