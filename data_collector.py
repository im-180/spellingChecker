class DataCollector:
    def __init__(self):
        """
        Initializes the DataCollector instance with an empty list for storing correct sentences.
        """
        self.correct_sentences = []

    def collect_data(self, correct_data_file):
        """
        Reads data from a specified file and populates the list of correct sentences.

        :param correct_data_file: Path to the file containing correct sentences.
        """
        # Open the file with the specified path and read it with UTF-8 encoding.
        with open(correct_data_file, 'r', encoding='utf-8') as file:
            # Iterate over each line in the file.
            for line in file:
                # Remove leading and trailing whitespace characters from the line.
                line = line.strip()
                # Check if the line is not empty after stripping whitespace.
                if line:
                    # Append the cleaned line to the list of correct sentences.
                    self.correct_sentences.append(line)

    def get_correct_sentences(self):
        """
        Returns the list of collected correct sentences.

        :return: List of strings, where each string is a correct sentence.
        """
        return self.correct_sentences
