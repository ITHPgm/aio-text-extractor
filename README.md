A complete Python application that acts as a Universal Text Extractor. To give it a premium, modern user interface, I will use the customtkinter library, which provides a sleek, dark-mode-ready desktop GUI.

The application will support extracting text from:

Plain Text files (.txt, .csv, etc.)

PDF files (.pdf)

Word Documents (.docx)

Images (.png, .jpg, .jpeg) using Optical Character Recognition (OCR).

How to Run this Premium App in VS Code
To make this work beautifully, you need to install a few Python libraries and an external tool for reading text from images (OCR).

Step 1: Install Tesseract-OCR (Required for Images)
Because you want to extract text from images, Python needs an underlying engine called Tesseract.

Windows: Download the installer from the UB-Mannheim Tesseract GitHub and install it. Note: If installed, check line 16 in the code to point Python to your installation path.

Mac (Homebrew): Open your terminal and run brew install tesseract

Linux (Ubuntu): Open your terminal and run sudo apt-get install tesseract-ocr

Step 2: Setup VS Code
Open VS Code.

Click File > New Text File, paste the python code above, and save it as text_extractor.py in a dedicated folder.

Open a Terminal inside VS Code by pressing Ctrl + ` (or going to Terminal > New Terminal from the top menu).

Step 3: Install Required Python Libraries
In that VS Code terminal, run the following command to install the premium UI library and the extraction dependencies:

Bash
pip install customtkinter PyPDF2 python-docx Pillow pytesseract
Step 4: Run the Application
Once the installations are complete, simply run the file. You can do this by:

Clicking the "Play" (Run Python File) button in the top right corner of VS Code.

OR, typing this into your VS Code terminal:

Bash
python text_extractor.py
