import tkinter as tk

class InputBox(tk.Toplevel):
    def __init__(self, parent, prompt):
        super().__init__(parent)
        self.title("Input")
        self.geometry("300x100")
        self.prompt = prompt
        self.result = None

        self.label = tk.Label(self, text=self.prompt)
        self.label.pack(pady=5)

        self.entry = tk.Entry(self)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.on_submit)

        self.submit_button = tk.Button(self, text="Submit", command=self.on_submit)
        self.submit_button.pack(pady=5)

    def on_submit(self, event=None):
        self.result = self.entry.get()
        self.destroy()

def get_input_from_msgbox(prompt):
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    input_box = InputBox(root, prompt)
    root.wait_window(input_box)  # Wait for the input box to close

    return input_box.result

def main():
    print("Please enter your message:")
    # Capture the input from the custom Tkinter message box
    message = get_input_from_msgbox("Enter your message:")
    # Simulate input() behavior
    print(f"You entered: {message}")

if __name__ == "__main__":
    main()