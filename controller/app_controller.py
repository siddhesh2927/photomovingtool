
from file_manager.search import FileSearcher
from file_manager.mover import FileMover
from file_manager.logger import AppLogger


class AppController:

    def __init__(self):


        self.searcher = FileSearcher()
        self.mover = FileMover()
        self.logger = AppLogger()

    def process(
            self,
            text_file_path,
            source_folder,
            destination_folder,
            prefix,
            extension,
            mode,
            progress_callback=None
    ):

        if progress_callback:
            progress_callback(0.10, "Reading numbers from text file...")

        numbers = []
        import re
        with open(text_file_path, "r", encoding="utf-8") as f:
            content = f.read()
            tokens = re.findall(r'[a-zA-Z0-9]+', content)
            seen = set()
            for token in tokens:
                token = token.upper()
                replacements = {"O": "0", "Q": "0", "D": "0", "I": "1", "L": "1", "|": "1", "S": "5", "B": "8", "Z": "2", "G": "6"}
                for old, new in replacements.items():
                    token = token.replace(old, new)
                token = re.sub(r"[^0-9]", "", token)
                
                if len(token) == 4 and token not in seen:
                    seen.add(token)
                    numbers.append({
                        "number": token,
                        "confidence": 100.0
                    })
        numbers.sort(key=lambda x: int(x["number"]))

        if progress_callback:
            progress_callback(0.40, "Searching photos...")

        matched, missing = self.searcher.find_files(
            numbers,
            source_folder,
            prefix,
            extension
        )

        if progress_callback:
            progress_callback(0.70, "Moving files...")

        moved, failed = self.mover.execute(
            matched,
            destination_folder,
            mode,
            progress_callback
        )

        log_path = self.logger.write_log(
            text_file_path=text_file_path,
            numbers=numbers,
            matched=matched,
            missing=missing,
            moved=moved,
            failed=failed
        )

        if progress_callback:
            progress_callback(1.0, "Completed")

        return {

            "numbers": numbers,

            "matched": matched,

            "missing": missing,

            "moved": moved,

            "failed": failed,

            "log": log_path

        }