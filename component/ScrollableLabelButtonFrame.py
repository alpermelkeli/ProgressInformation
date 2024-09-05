import customtkinter as ctk

class ScrollableLabelButtonFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, edit_command=None,export_command = None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.edit_command = edit_command
        self.export_command = export_command
        self.id_list = []
        self.label_list = []
        self.edit_button_list = []
        self.export_button_list = []
        self.progress_list = []

    def add_item(self, item_id, item_name, progress=0, image=None):
        label = ctk.CTkLabel(self, text=item_name, image=image, compound="left", padx=5, anchor="w")
        progress_label = ctk.CTkLabel(self, text=f"%{progress:.2f}", padx=5, anchor="w")
        edit_button = ctk.CTkButton(self, text="Düzenle", width=75, height=24)
        export_button = ctk.CTkButton(self, text="Birleştir", width=75, height=24)

        if self.edit_command is not None:
            edit_button.configure(command=lambda: self.edit_command(item_id))

        if self.export_command is not None:
            export_button.configure(command=lambda: self.export_command(item_id))

        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        progress_label.grid(row=len(self.progress_list), column=1, pady=(0, 10), padx=5, sticky="w")
        edit_button.grid(row=len(self.edit_button_list), column=2, pady=(0, 10), padx=5)
        export_button.grid(row=len(self.export_button_list), column=3, pady=(0, 10), padx=5)
        self.id_list.append(item_id)
        self.label_list.append(label)
        self.edit_button_list.append(edit_button)
        self.export_button_list.append(export_button)
        self.progress_list.append(progress_label)

    def update_progress(self, id, progress):
        for item_id, progress_label in zip(self.id_list, self.progress_list):
            if item_id == id:
                progress_label.configure(text=f"%{progress:.2f}")
                return

    def remove_item(self, item):
        for label, edit_button, export_button, progress_label in zip(self.label_list, self.edit_button_list, self.export_button_list, self.progress_list):
            label.destroy()
            edit_button.destroy()
            export_button.destroy()
            progress_label.destroy()
            self.label_list.remove(label)
            self.edit_button_list.remove(edit_button)
            self.export_button_list.remove(export_button)
            self.progress_list.remove(progress_label)
