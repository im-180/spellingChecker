import tkinter as tk
from tkinter import filedialog, messagebox

from integration import SpellChecker
from test_evaluation import Evaluator 

class SpellCheckerGUI:
    def __init__(self, root):
        """
        Initializes the GUI for the Spell Checker application.

        :param root: The root Tkinter window instance.
        """
        self.root = root
        self.root.title("English Spell Checker with Context-Awareness")  # Set the window title
        self.root.geometry("700x400")  # Set the window size
        self.root.configure(bg="#f0f0f0")  # Set background color of the window

        # Initialize SpellChecker and Evaluator instances
        self.spell_checker = SpellChecker()
        self.evaluator = Evaluator(self.spell_checker)

        # Define styles for the GUI components
        self.font_style = ("Helvetica", 14)
        self.button_style = {"font": ("Helvetica", 12, "bold"), "bg": "#4CAF50", "fg": "white", "bd": 0, "padx": 10, "pady": 5}
        self.label_style = {"font": self.font_style, "bg": "#f0f0f0"}
        self.entry_style = {"font": self.font_style, "bg": "white", "fg": "black", "wrap": "word", "bd": 2, "relief": "sunken"}
        self.frame_style = {"bg": "#f0f0f0"}

        # Frame for training model
        self.train_frame = tk.Frame(root, **self.frame_style)
        self.train_frame.pack(pady=10)

        # Button to trigger model training
        self.train_button = tk.Button(self.train_frame, text="Train Model", command=self.train_model, **self.button_style)
        self.train_button.pack()

        # Frame for input text
        self.input_frame = tk.Frame(root, **self.frame_style)
        self.input_frame.pack(pady=10)

        # Label and text area for user input
        self.input_label = tk.Label(self.input_frame, text="Enter Text:", **self.label_style)
        self.input_label.pack(pady=5)
        self.input_text = tk.Text(self.input_frame, width=70, height=3, **self.entry_style)  # Reduced height for input area
        self.input_text.pack(pady=10)

        # Frame for checking paragraph
        self.check_frame = tk.Frame(root, **self.frame_style)
        self.check_frame.pack(pady=10)

        # Button to trigger paragraph checking
        self.check_button = tk.Button(self.check_frame, text="Check Spelling", command=self.check_paragraph, **self.button_style)
        self.check_button.pack()

        # Frame for displaying results
        self.output_frame = tk.Frame(root, **self.frame_style)
        self.output_frame.pack(pady=10)

        # Label for showing the results
        self.output_label = tk.Label(self.output_frame, text="", **self.label_style)
        self.output_label.pack(pady=10)

    def train_model(self):
        """
        Opens a file dialog to select a training data file and trains the spell checker model.
        Displays a message box when training is complete.
        """
        correct_data_file = filedialog.askopenfilename(title="Select Training Data File")
        if correct_data_file:
            self.spell_checker.train(correct_data_file)
            messagebox.showinfo("Training Complete", "The model has been trained successfully.")
            self.test_model()  # Ensure the model is tested after training

    def check_paragraph(self):
        """
        Retrieves the text from the input field, checks it for spelling errors, and displays the results.
        """
        paragraph = self.input_text.get("1.0", tk.END).strip()
        if not paragraph:
            messagebox.showwarning("Input Error", "Please type a sentence to test.")
            return
        
        corrections = self.spell_checker.check(paragraph)
        if not corrections:
            self.output_label.config(text="Congratulations!  No mistakes found.", fg="green")
        else:
            corrections_text = "\n".join([f"{word}: {info}" for word, info in corrections])
            self.output_label.config(text=f"Corrections:\n{corrections_text}", fg="red")

    def test_model(self):
        """
        Tests the trained model with predefined sentences and displays evaluation metrics.
        """
        test_sentences = [
            "I would like to accommodate his wishes.",
            "He was amondg the living.",
            "The two politicians godt into a heatedd argument.",
            "The boy is quickly becoming a man.",
            "I beliedve in magic.",
            "The goodd citizven votes in every elecdtion.",
            "It happened durving the night.",
            "Their car is parked in the driveway.",
            "The kevys are over there on the counter."
        ]

        true_errors = [
            [],  # No errors 
            ["amondg"],  
            ["godt", "heatedd"], 
            ["beliedve"],  
            ["goodd", "citizven", "elecdtion"], 
            ["durving"],  
            [],  
            ["kevys"]  
        ]

        # Evaluate the spell checker and display the results
        precision, recall, f1_score, accuracy = self.evaluator.evaluate(test_sentences, true_errors)
        result_text = (
            f"Evaluation Results:\n"
            f"Precision: {precision:.2f}\n"
            f"Recall: {recall:.2f}\n"
            f"F1 Score: {f1_score:.2f}\n"
            f"Accuracy: {accuracy:.2f}"
        )
        print(result_text)  # Print evaluation results to the console

if __name__ == "__main__":
    # Create the main window and start the Tkinter event loop
    root = tk.Tk()
    app = SpellCheckerGUI(root)
    root.mainloop()
