import customtkinter as ctk
import pyperclip


class ScrollableLabelButtonFrameRender(ctk.CTkScrollableFrame):
    def __init__(self, master, edit_command=None, remove_command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)

        self.edit_command = edit_command
        self.remove_command = remove_command
        self.id_list = []
        self.label_list = []
        self.edit_button_list = []
        self.progress_list = []
        self.remove_button_list = []
        self.link_button_list = []

        self.header_label = ctk.CTkLabel(self, text="Render", font=("Arial", 16, "bold"), padx=5, pady=10)
        self.header_label.grid(row=0, column=0, columnspan=6, pady=(0, 10), sticky="ew")

    def add_item(self, item_id, item_name, progress=0, image=None):
        row_index = len(self.label_list) + 1

        label = ctk.CTkLabel(self, text=item_name, image=image, compound="left", padx=5, anchor="w")
        progress_label = ctk.CTkLabel(self, text=f"%{progress:.2f}", padx=5, anchor="w")
        edit_button = ctk.CTkButton(self, text="Düzenle", width=75, height=24)
        remove_button = ctk.CTkButton(self, text="Sil", width=75, height=24)
        link_button = ctk.CTkButton(self, text="Copy Link", width=75, height=24,
                                    command=lambda: self.copy_to_clipboard(f"http://34.44.221.30:5000/project/{item_id}"))
        if self.edit_command is not None:
            edit_button.configure(command=lambda: self.edit_command(item_id))

        if self.remove_command is not None:
            remove_button.configure(command=lambda: self.remove_command(item_id))

        # Arrange widgets in the grid
        label.grid(row=row_index, column=0, pady=(0, 10), sticky="w")
        progress_label.grid(row=row_index, column=1, pady=(0, 10), padx=5, sticky="w")
        edit_button.grid(row=row_index, column=2, pady=(0, 10), padx=5)
        remove_button.grid(row=row_index, column=3, pady=(0, 10), padx=5)
        link_button.grid(row=row_index, column=4, pady=(0, 10), padx=5, sticky="w")

        # Append elements to their respective lists
        self.id_list.append(item_id)
        self.label_list.append(label)
        self.edit_button_list.append(edit_button)
        self.progress_list.append(progress_label)
        self.remove_button_list.append(remove_button)
        self.link_button_list.append(link_button)
    def update_progress(self, id, progress):
        for item_id, progress_label in zip(self.id_list, self.progress_list):
            if item_id == id:
                progress_label.configure(text=f"%{progress:.2f}")
                return
    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
    def remove_item(self, item_id):
        for index, current_id in enumerate(self.id_list):
            if current_id == item_id:
                # Destroy all elements related to the project
                self.label_list[index].destroy()
                self.edit_button_list[index].destroy()
                self.progress_list[index].destroy()
                self.remove_button_list[index].destroy()
                self.link_button_list[index].destroy()

                # Remove from lists
                self.id_list.pop(index)
                self.label_list.pop(index)
                self.edit_button_list.pop(index)
                self.progress_list.pop(index)
                self.remove_button_list.pop(index)
                self.link_button_list.pop(index)
                break
