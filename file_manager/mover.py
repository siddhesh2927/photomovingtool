import shutil
from pathlib import Path


class FileMover:

    def execute(
        self,
        matched_files,
        destination_folder,
        mode,
        progress_callback=None
    ):

        destination = Path(destination_folder)
        destination.mkdir(parents=True, exist_ok=True)

        moved = []

        failed = []

        total = len(matched_files)

        for index, file in enumerate(matched_files):

            source = Path(file["source"])
            destination_file = destination / source.name

            try:

                if mode == "move":
                    shutil.move(source, destination_file)
                else:
                    shutil.copy2(source, destination_file)

                moved.append({
                    "filename": source.name,
                    "number": file["number"]
                })

            except Exception as e:

                failed.append(
                    {
                        "filename": source.name,
                        "error": str(e)
                    }
                )
            
            if progress_callback:

                percent = (index + 1) / total

                progress_callback(
                    percent,
                    f"{index+1}/{total} : {source.name}"
                )

        return moved, failed