import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from controller.app_controller import AppController


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class PhotoMoverApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Photo Mover")
        self.geometry("900x720")
        self.resizable(False, False)

        self.controller = AppController()

        self.text_file_path = ""
        self.source_folder = ""
        self.destination_folder = ""

        self.create_widgets()

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="📷 Photo Mover",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(pady=20)

        self.build_file_selector(
            "Numbers Text File",
            self.browse_text_file
        )

        self.build_file_selector(
            "Source Folder",
            self.browse_source
        )

        self.build_file_selector(
            "Destination Folder",
            self.browse_destination
        )

        options = ctk.CTkFrame(self)
        options.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            options,
            text="Prefix"
        ).grid(row=0, column=0, padx=10, pady=10)

        self.prefix = ctk.CTkEntry(
            options,
            width=120
        )
        self.prefix.insert(0, "DSC_")
        self.prefix.grid(row=0, column=1)

        ctk.CTkLabel(
            options,
            text="Extension"
        ).grid(row=0, column=2, padx=(30, 5))

        self.extension = ctk.CTkComboBox(
            options,
            values=[".jpg", ".jpeg", ".png"]
        )
        self.extension.set(".jpg")
        self.extension.grid(row=0, column=3)

        self.mode = ctk.StringVar(value="move")

        move_radio = ctk.CTkRadioButton(
            options,
            text="Move",
            variable=self.mode,
            value="move"
        )
        move_radio.grid(row=0, column=4, padx=(30, 10))

        copy_radio = ctk.CTkRadioButton(
            options,
            text="Copy",
            variable=self.mode,
            value="copy"
        )
        copy_radio.grid(row=0, column=5)

        ctk.CTkLabel(
            self,
            text="Output",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=(15, 5))

        self.output = ctk.CTkTextbox(
            self,
            width=820,
            height=250
        )
        self.output.pack()

        self.progress = ctk.CTkProgressBar(
            self,
            width=820
        )
        self.progress.pack(pady=20)
        self.progress.set(0)

        self.status = ctk.CTkLabel(
            self,
            text="Waiting..."
        )
        self.status.pack()

        self.start_btn = ctk.CTkButton(
            self,
            text="START",
            width=220,
            height=45,
            command=lambda: threading.Thread(
                target=self.start_process,
                daemon=True
            ).start()
        )
        self.start_btn.pack(pady=20)

    def build_file_selector(self, text, command):

        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=20, pady=8)

        label = ctk.CTkLabel(
            frame,
            text=text,
            width=160,
            anchor="w"
        )
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(
            frame,
            width=500
        )
        entry.pack(side="left", padx=10)

        button = ctk.CTkButton(
            frame,
            text="Browse",
            width=120,
            command=command
        )
        button.pack(side="right", padx=10)

        if text == "Numbers Text File":
            self.text_file_entry = entry

        elif text == "Source Folder":
            self.source_entry = entry

        elif text == "Destination Folder":
            self.destination_entry = entry

    def browse_text_file(self):

        path = filedialog.askopenfilename(
            filetypes=[
                ("Text Files", "*.txt")
            ]
        )

        if path:
            self.text_file_path = path
            self.text_file_entry.delete(0, "end")
            self.text_file_entry.insert(0, path)

    def browse_source(self):

        folder = filedialog.askdirectory()

        if folder:
            self.source_folder = folder
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, folder)

    def browse_destination(self):

        folder = filedialog.askdirectory()

        if folder:
            self.destination_folder = folder
            self.destination_entry.delete(0, "end")
            self.destination_entry.insert(0, folder)

    def update_progress(self, value, message):

        self.after(
            0,
            lambda: self.progress.set(value)
        )

        self.after(
            0,
            lambda: self.status.configure(text=message)
        )

    def start_process(self):

        if not self.text_file_path:
            messagebox.showerror(
                "Error",
                "Please select a numbers text file."
            )
            return

        if not self.source_folder:
            messagebox.showerror(
                "Error",
                "Please select the source folder."
            )
            return

        if not self.destination_folder:
            messagebox.showerror(
                "Error",
                "Please select the destination folder."
            )
            return

        self.output.delete("1.0", "end")
        self.progress.set(0)
        self.status.configure(text="Processing...")

        self.update()

        try:

            result = self.controller.process(
                text_file_path=self.text_file_path,
                source_folder=self.source_folder,
                destination_folder=self.destination_folder,
                prefix=self.prefix.get(),
                extension=self.extension.get(),
                mode=self.mode.get(),
                progress_callback=self.update_progress
            )

            self.output.insert("end", "===== Extracted Numbers =====\n\n")

            for item in result["numbers"]:
                self.output.insert("end", f"{item['number']}\n")

            self.output.insert("end", "\n=============================\n\n")

            self.output.insert(
                "end",
                f"Matched Files : {len(result['matched'])}\n"
            )

            self.output.insert(
                "end",
                f"Moved Files   : {len(result['moved'])}\n"
            )

            self.output.insert(
                "end",
                f"Missing Files : {len(result['missing'])}\n\n"
            )

            if result["missing"]:

                self.output.insert("end", "Missing Files\n")
                self.output.insert("end", "-------------------------\n")

                for file in result["missing"]:
                    self.output.insert("end", file + "\n")

            self.output.insert(
                "end",
                f"\n\nLog Saved:\n{result['log']}"
            )

            self.progress.set(1)
            self.status.configure(text="Completed Successfully")

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

            self.status.configure(text="Failed")