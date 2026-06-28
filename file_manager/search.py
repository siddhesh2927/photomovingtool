from pathlib import Path


class FileSearcher:

    def __init__(self):
        self.file_index = {}
        self.last_source_folder = ""

    def build_index(self, source_folder):

        self.file_index.clear()

        source = Path(source_folder)

        if not source.exists():
            raise Exception("Source folder does not exist.")

        for file in source.iterdir():

            if not file.is_file():
                continue

            # Store filename without extension
            self.file_index[file.stem.upper()] = str(file)

        print(f"Indexed {len(self.file_index)} files.")

    def find_files(
        self,
        numbers,
        source_folder,
        prefix,
        extension
    ):

        # Build index if empty or folder changed
        if not self.file_index or self.last_source_folder != source_folder:
            self.build_index(source_folder)
            self.last_source_folder = source_folder

        matched = []
        missing = []

        for item in numbers:

            number = item["number"]

            filename = f"{prefix}{number}"

            if filename.upper() in self.file_index:

                matched.append(
                    {
                        "number": number,
                        "confidence": item["confidence"],
                        "source": self.file_index[filename.upper()],
                        "filename": filename + extension
                    }
                )

            else:

                missing.append(
                    {
                        "number": number,
                        "filename": filename + extension
                    }
                )

        return matched, missing