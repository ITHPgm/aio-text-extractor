import customtkinter as ctk
from tkinter import filedialog
import os
import threading

# Import extraction libraries
import PyPDF2
import docx
from PIL import Image
import pytesseract

# Set the overall appearance to dark mode with a blue accent theme for a premium look
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# NOTE FOR WINDOWS USERS:
# If you are on Windows, you MUST install the Tesseract executable and point to its location.
# Uncomment and modify the line below if you get a "tesseract is not installed" error.
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class TextExtractorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("Universal Text Extractor Pro")
        self.geometry("900x650")
        self.minsize(700, 500)
        self.selected_file_path = None

        # Configure grid layout (1 column, 3 main rows)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Header Section ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.header_frame.grid_columnconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="Text Extractor Pro", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        # --- File Selection Section ---
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.file_frame.grid_columnconfigure(1, weight=1)

        self.select_btn = ctk.CTkButton(
            self.file_frame, 
            text="Choose File", 
            command=self.select_file,
            font=ctk.CTkFont(weight="bold")
        )
        self.select_btn.grid(row=0, column=0, padx=20, pady=20)

        self.file_path_label = ctk.CTkLabel(
            self.file_frame, 
            text="No file selected...", 
            text_color="gray"
        )
        self.file_path_label.grid(row=0, column=1, padx=(0, 20), sticky="w")

        self.extract_btn = ctk.CTkButton(
            self.file_frame, 
            text="Extract Text", 
            command=self.start_extraction,
            fg_color="#2ECC71",
            hover_color="#27AE60",
            font=ctk.CTkFont(weight="bold"),
            state="disabled"
        )
        self.extract_btn.grid(row=0, column=2, padx=20, pady=20)

        # --- Output Section ---
        self.textbox = ctk.CTkTextbox(
            self, 
            font=ctk.CTkFont(family="Consolas", size=14),
            wrap="word"
        )
        self.textbox.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="nsew")

        # --- Footer Section ---
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.footer_frame.grid_columnconfigure(0, weight=1)

        self.copy_btn = ctk.CTkButton(
            self.footer_frame, 
            text="Copy to Clipboard", 
            command=self.copy_to_clipboard,
            state="disabled"
        )
        self.copy_btn.grid(row=0, column=1, sticky="e")
        
        self.status_label = ctk.CTkLabel(self.footer_frame, text="Ready", text_color="gray")
        self.status_label.grid(row=0, column=0, sticky="w")

    def select_file(self):
        filetypes = (
            ("All Supported Files", "*.txt *.pdf *.docx *.png *.jpg *.jpeg"),
            ("Text Files", "*.txt"),
            ("PDF Files", "*.pdf"),
            ("Word Documents", "*.docx"),
            ("Images (OCR)", "*.png *.jpg *.jpeg"),
            ("All Files", "*.*")
        )
        filepath = filedialog.askopenfilename(title="Select a file", filetypes=filetypes)
        
        if filepath:
            self.selected_file_path = filepath
            # Shorten display path if too long
            display_path = filepath if len(filepath) < 50 else f"...{filepath[-47:]}"
            self.file_path_label.configure(text=display_path, text_color="white")
            self.extract_btn.configure(state="normal")
            self.textbox.delete("1.0", "end")
            self.status_label.configure(text="File loaded. Ready to extract.")

    def copy_to_clipboard(self):
        extracted_text = self.textbox.get("1.0", "end-1c")
        if extracted_text:
            self.clipboard_clear()
            self.clipboard_append(extracted_text)
            self.status_label.configure(text="Copied to clipboard!")

    def start_extraction(self):
        self.status_label.configure(text="Extracting text, please wait...")
        self.textbox.delete("1.0", "end")
        self.extract_btn.configure(state="disabled")
        self.select_btn.configure(state="disabled")
        
        # Run extraction in a separate thread to keep UI responsive
        threading.Thread(target=self.process_file, daemon=True).start()

    def process_file(self):
        path = self.selected_file_path
        ext = os.path.splitext(path)[1].lower()
        extracted_text = ""

        try:
            if ext == '.txt':
                extracted_text = self.extract_from_txt(path)
            elif ext == '.pdf':
                extracted_text = self.extract_from_pdf(path)
            elif ext == '.docx':
                extracted_text = self.extract_from_docx(path)
            elif ext in ['.png', '.jpg', '.jpeg']:
                extracted_text = self.extract_from_image(path)
            else:
                extracted_text = "Unsupported file format."
        except Exception as e:
            extracted_text = f"An error occurred during extraction:\n{str(e)}"

        # Schedule the UI update back on the main thread
        self.after(0, self.update_ui_post_extraction, extracted_text)

    def extract_from_txt(self, path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()

    def extract_from_pdf(self, path):
        text = ""
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        return text if text else "No text could be parsed from this PDF. It might be scanned (requires OCR)."

    def extract_from_docx(self, path):
        doc = docx.Document(path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    def extract_from_image(self, path):
        img = Image.open(path)
        # Tesseract handles the OCR magic here
        text = pytesseract.image_to_string(img)
        return text if text.strip() else "No text found in the image."

    def update_ui_post_extraction(self, text):
        self.textbox.insert("1.0", text)
        self.status_label.configure(text="Extraction complete.")
        self.extract_btn.configure(state="normal")
        self.select_btn.configure(state="normal")
        self.copy_btn.configure(state="normal")


if __name__ == "__main__":
    app = TextExtractorApp()
    app.mainloop()
