import re #supports for regular expressions 

class TextPreprocessor:
    def __init__(self):
        """
        Initializes the TextPreprocessor instance.
        """
        pass

    def tokenize(self, text):
        """
        Tokenizes the input text into a list of words.

        :param text: The input string to be tokenized.
        :return: A list of lowercase words from the input text.
        """
        # Convert the entire text to lowercase and then split it into words based on whitespace.
        return text.lower().split()

    def preprocess(self, sentences):
        """
        Applies preprocessing steps to a list of sentences.

        :param sentences: A list of sentences, where each sentence is a string.
        :return: A list of tokenized sentences, where each sentence is represented as a list of words.
        """
        # Process each sentence in the list by tokenizing it.
        return [self.tokenize(sentence) for sentence in sentences]

    def preprocess_text(self, text):
        """
        Applies various preprocessing steps to a single text string.

        :param text: The input string to be preprocessed.
        :return: A preprocessed string with lowercase conversion, removal of numbers, and punctuation.
        """
        # Convert the entire text to lowercase.
        text = text.lower()
        # Remove all numbers from the text using a regular expression.
        text = re.sub(r'\d+', '', text)
        # Remove all punctuation characters from the text using a regular expression.
        text = re.sub(r'[^\w\s]', '', text)
        return text


