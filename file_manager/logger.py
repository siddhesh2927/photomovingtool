from pathlib import Path
from datetime import datetime


class AppLogger:

    def __init__(self):

        self.log_folder = Path("logs")
        self.log_folder.mkdir(exist_ok=True)

    def write_log(
            self,
            text_file_path,
            numbers,
            matched,
            missing,
            moved,
            failed
    ):

        filename = datetime.now().strftime(
            "Run_%Y%m%d_%H%M%S.txt"
        )

        logfile = self.log_folder / filename

        with open(logfile, "w", encoding="utf-8") as file:

            file.write("=" * 60 + "\n")
            file.write("PHOTO MOVER LOG\n")
            file.write("=" * 60 + "\n\n")

            file.write(f"Input Text File : {text_file_path}\n\n")

            file.write("-" * 60 + "\n")
            file.write("Detected Numbers\n")
            file.write("-" * 60 + "\n")

            for item in numbers:

                file.write(
                    f"{item['number']}   "
                    f"({item['confidence']:.2f}%)\n"
                )

            file.write("\n")

            file.write("-" * 60 + "\n")
            file.write("Matched Files\n")
            file.write("-" * 60 + "\n")

            for item in matched:

                file.write(item["filename"] + "\n")

            file.write("\n")

            file.write("-" * 60 + "\n")
            file.write("Missing Files\n")
            file.write("-" * 60 + "\n")

            for item in missing:

                file.write(item["filename"] + "\n")

            file.write("\n")

            file.write("-" * 60 + "\n")
            file.write("Moved Files\n")
            file.write("-" * 60 + "\n")

            for item in moved:

                file.write(item["filename"] + "\n")

            file.write("\n")

            file.write("-" * 60 + "\n")
            file.write("Failed\n")
            file.write("-" * 60 + "\n")

            for item in failed:

                file.write(
                    f"{item['filename']} : "
                    f"{item['error']}\n"
                )

        return str(logfile)