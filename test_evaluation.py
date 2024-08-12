
class Evaluator:
    def __init__(self, spell_checker):
        """
        Initializes the Evaluator with a SpellChecker instance.

        :param spell_checker: An instance of the SpellChecker class to be used for checking sentences.
        """
        self.spell_checker = spell_checker

    def evaluate(self, test_sentences, true_errors):
        """
        Evaluates the spell checker using given test sentences and known errors.

        :param test_sentences: List of sentences to test.
        :param true_errors: List of lists containing the true spelling errors for each sentence.
        :return: Precision, Recall, F1 Score, Accuracy
        """
        predicted_errors = []  # To store errors predicted by the spell checker
        
        # Check each sentence using the spell checker
        for sentence in test_sentences:
            corrections = self.spell_checker.check(sentence)
            # Extract words with issues from corrections
            errors = [correction[0] for correction in corrections if correction[1] == "Misspelling"]
            predicted_errors.append(errors)
        
        tp, fp, fn, tn = 0, 0, 0, 0  # Initialize counts for true positives, false positives, false negatives, and true negatives
        total_errors = 0  # To keep track of total number of errors

        # Calculate TP, FP, FN for each sentence
        for pred_errors, true_errors_list in zip(predicted_errors, true_errors):
            total_errors += len(true_errors_list)
            
            pred_set = set(pred_errors)
            true_set = set(true_errors_list)
            
            tp += len(pred_set & true_set)  # tp =true +ve
            fp += len(pred_set - true_set)  # fp =false +ve
            fn += len(true_set - pred_set)  

        # Calculate Precision
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        
        # Calculate Recall
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        
        # Calculate F1 Score
        f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        # Accuracy calculation is not straightforward in this context; use errors as a reference
        accuracy = (tp + tn) / total_errors if total_errors > 0 else 0

        return precision, recall, f1_score, accuracy

