# Photo Mover

Photo Mover is a GUI application built with Python and `customtkinter`. It allows users to read a list of numbers from a text file, search for corresponding photos (with a specific prefix and extension) in a source directory, and move or copy them to a destination directory.

## Features

- **User-Friendly GUI**: Built using `customtkinter` for a modern, dark-themed interface.
- **Batch Processing**: Move or copy multiple photos at once.
- **Smart Text Parsing**: Extracts 4-digit numbers from a text file, applying common OCR error corrections (e.g., 'O' to '0', 'S' to '5').
- **Customizable Prefix and Extension**: Search for files with specific prefixes (e.g., `DSC_`) and extensions (e.g., `.jpg`, `.png`).
- **Detailed Logging**: Keeps track of matched files, missing files, moved files, and errors.

## Requirements

The dependencies can be installed using:

```bash
pip install -r requirements.txt
```

Current dependencies include:
- `customtkinter`
- `opencv-python`
- `Pillow`
- `numpy`
- `paddlepaddle`
- `paddleocr`
- `pytesseract` (Added for future Tesseract OCR integrations)

## How to Run

Execute the main script to launch the application:

```bash
python main.py
```

## Usage

1. **Numbers Text File**: Browse and select a `.txt` file containing the numbers of the photos you want to move/copy.
2. **Source Folder**: Browse and select the directory containing the original photos.
3. **Destination Folder**: Browse and select the directory where you want the photos to be moved or copied.
4. **Prefix & Extension**: Specify the prefix (e.g., `DSC_`) and the file extension (e.g., `.jpg`).
5. **Mode**: Choose whether to **Move** or **Copy** the files.
6. **Start**: Click the START button to begin the process. The application will output the matched, moved, and missing files and generate a log.

## Future Upgrades
- Integration with `pytesseract` for advanced OCR capabilities directly from images.
