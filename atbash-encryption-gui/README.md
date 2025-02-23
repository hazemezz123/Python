# Atbash Encryption GUI

This project provides a graphical user interface (GUI) for the Atbash encryption algorithm using Tkinter. The Atbash cipher is a simple substitution cipher that replaces each letter in the plaintext with its reverse in the alphabet.

## Project Structure

```
atbash-encryption-gui
├── src
│   ├── main.py        # Entry point of the application
│   ├── atbash.py      # Contains the Atbash encryption function
├── requirements.txt    # Lists the dependencies required for the project
└── README.md           # Documentation for the project
```

## Requirements

To run this project, you need to have Python installed along with the following libraries:

- Tkinter (usually included with Python installations)
- Any other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install the required dependencies using pip:

   ```
   pip install -r requirements.txt
   ```

## Running the Application

To run the application, execute the following command:

```
python src/main.py
```

This will open the Atbash encryption GUI where you can enter text to be encrypted.

## Packaging as .exe

To package the application as a .exe file for Windows, you can use a tool like PyInstaller. Follow these steps:

1. Install PyInstaller if you haven't already:

   ```
   pip install pyinstaller
   ```

2. Navigate to the `src` directory:

   ```
   cd src
   ```

3. Run PyInstaller to create the executable:

   ```
   pyinstaller --onefile main.py
   ```

4. After the process completes, you will find the .exe file in the `dist` folder.

## License

This project is open-source and available under the MIT License.