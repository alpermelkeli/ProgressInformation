import customtkinter as ctk

from tkinter import filedialog, messagebox

import threading

import time

import os

from utils.Export import export_project
from utils.Upload import upload_project

import requests

from component.ScrollableLabelButtonFrameAnimation import ScrollableLabelButtonFrameAnimation

from component.ScrollableLabelButtonFrameRender import ScrollableLabelButtonFrameRender


from model.Project import Project

ADD_PROJECT_URL = "http://34.44.221.30:5000/addProject"
REMOVE_PROJECT_URL = "http://34.44.221.30:5000/removeProject"

class ProjectTrackerApp:
    def __init__(self, root):
        self.dynamic_fields_frame = None

        self.root = root

        self.root.title("Project Tracker")

        self.projects = []

        self.animation_frame = ScrollableLabelButtonFrameAnimation(root, edit_command=self.edit_selected_project,
                                                          export_command=self.export_selected_project,
                                                          remove_command=self.remove_project, width=750, height=250)

        self.render_frame = ScrollableLabelButtonFrameRender(root, edit_command=self.edit_selected_project,
                                                             remove_command=self.remove_project, width=750, height=250)

        self.animation_frame.pack(pady=10)
        self.render_frame.pack(pady=10)

        self.add_project_button = ctk.CTkButton(root, text="Yeni Proje Ekle", command=self.add_project)
        self.add_project_button.pack(pady=10)

    def add_project(self):
        new_project_window = ctk.CTkToplevel(self.root)
        new_project_window.title("Yeni Proje Ekle")

        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        new_project_window.geometry(f"{root_width}x{root_height+100}+{root_x}+{root_y}")
        new_project_window.focus_set()
        new_project_window.grab_set()

        ctk.CTkLabel(new_project_window, text="Proje Türü:").pack()
        project_type_var = ctk.StringVar(value="Animation")
        ctk.CTkRadioButton(
            new_project_window, height=50,text="Animation", variable=project_type_var, value="Animation",
            command=lambda: self.update_project_fields(new_project_window, project_type_var.get())
        ).pack()
        ctk.CTkRadioButton(
            new_project_window, height=50,text="Render", variable=project_type_var, value="Render",
            command=lambda: self.update_project_fields(new_project_window, project_type_var.get())
        ).pack()

        self.dynamic_fields_frame = ctk.CTkFrame(new_project_window,height=250)
        self.dynamic_fields_frame.pack(fill="both", expand=False)

        self.update_project_fields(new_project_window, project_type_var.get())

        ctk.CTkLabel(new_project_window, text="Proje İsmi:").pack()
        project_name_entry = ctk.CTkEntry(new_project_window)
        project_name_entry.pack()

        ctk.CTkLabel(new_project_window, text="Klasör Konumu:").pack()
        folder_path_entry = ctk.CTkEntry(new_project_window)
        folder_path_entry.pack()
        folder_browse_button = ctk.CTkButton(new_project_window, text="Gözat",
                                             command=lambda: self.browse_folder(folder_path_entry))
        folder_browse_button.pack()

        ctk.CTkLabel(new_project_window, text="Toplam Dosya Sayısı:").pack()
        total_files_entry = ctk.CTkEntry(new_project_window)
        total_files_entry.pack()

        ctk.CTkLabel(new_project_window, text="Bilgilendirme Mesajı:").pack()
        notification_message_entry = ctk.CTkEntry(new_project_window)
        notification_message_entry.pack()

        ctk.CTkLabel(new_project_window, text="Ödeme Linki:").pack()
        payment_link_entry = ctk.CTkEntry(new_project_window)
        payment_link_entry.pack()

        ctk.CTkLabel(new_project_window, text="GPU Sayısı:").pack()
        gpu_count_entry = ctk.CTkEntry(new_project_window)
        gpu_count_entry.pack()

        ctk.CTkLabel(new_project_window, text="Fiyat:").pack()
        price_entry = ctk.CTkEntry(new_project_window)
        price_entry.pack()

        add_button = ctk.CTkButton(
            new_project_window, text="Ekle",
            command=lambda: self.save_project(
                new_project_window, project_name_entry, folder_path_entry, total_files_entry,
                notification_message_entry, payment_link_entry, gpu_count_entry, price_entry,
                project_type_var.get(),self.resolution_entry,self.frame_count_entry
            )
        )
        add_button.pack(pady=10)

    def update_project_fields(self, window, project_type):
        for widget in self.dynamic_fields_frame.winfo_children():
            widget.destroy()

        if project_type == "Animation":

            ctk.CTkLabel(self.dynamic_fields_frame, text="Çözünürlük:").pack()
            self.resolution_entry = ctk.CTkOptionMenu(self.dynamic_fields_frame,values=["640x360", "1280x720", "1920x1080", "2560x1440", "3840x2160"])
            self.resolution_entry.pack()

            ctk.CTkLabel(self.dynamic_fields_frame, text="fps:").pack()
            self.frame_count_entry = ctk.CTkOptionMenu(self.dynamic_fields_frame, values=["25", "30", "60", "200"])
            self.frame_count_entry.pack()
        elif project_type == "Render":

            ctk.CTkLabel(self.dynamic_fields_frame, text="Çözünürlük:").pack()
            self.resolution_entry = ctk.CTkOptionMenu(self.dynamic_fields_frame,values=["640x360", "1280x720", "1920x1080", "2560x1440", "3840x2160"])
            self.resolution_entry.pack()

    @staticmethod
    def browse_folder(entry):
        folder_path = filedialog.askdirectory()
        if folder_path:
            entry.delete(0, ctk.END)
            entry.insert(0, folder_path)

    def save_project(self, window, name_entry, folder_entry, total_files_entry, message_entry, link_entry,
                     gpu_count_entry, price_entry, project_type, resolution_entry,frame_count_entry):
        name = name_entry.get()
        folder_path = folder_entry.get()
        total_files = int(total_files_entry.get())
        notification_message = message_entry.get()
        payment_link = link_entry.get()
        gpu_count = gpu_count_entry.get()
        price = price_entry.get()
        resolution = resolution_entry.get()
        fps = frame_count_entry.get()

        if name and folder_path and total_files and notification_message:
            new_project = Project(name, folder_path, total_files, notification_message, payment_link,
                                  gpu_count=gpu_count, price=price, project_type=project_type, resolution=resolution,fps=fps)
            self.projects.append(new_project)

            target_frame = self.animation_frame if project_type == "Animation" else self.render_frame
            target_frame.add_item(new_project.id, new_project.name)

            threading.Thread(target=self.track_project, args=(new_project, target_frame.update_progress)).start()

            window.destroy()
        else:
            messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun.")
    def edit_selected_project(self, project_id):
        selected_project = next((project for project in self.projects if project.id == project_id), None)
        if selected_project is None:
            messagebox.showwarning("Hata", "Seçilen proje bulunamadı.")
            return
        edit_window = ctk.CTkToplevel(self.root)
        edit_window.title("Projeyi Düzenle")

        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        edit_window.geometry(f"{root_width}x{root_height}+{root_x}+{root_y}")
        edit_window.focus_set()
        edit_window.grab_set()

        ctk.CTkLabel(edit_window, text="Proje İsmi:").pack()
        project_name_entry = ctk.CTkEntry(edit_window)
        project_name_entry.insert(0, selected_project.name)
        project_name_entry.pack()

        ctk.CTkLabel(edit_window, text="Klasör Konumu:").pack()
        folder_path_entry = ctk.CTkEntry(edit_window)
        folder_path_entry.insert(0, selected_project.folder_path)
        folder_path_entry.pack()
        folder_browse_button = ctk.CTkButton(edit_window, text="Gözat",
                                             command=lambda: self.browse_folder(folder_path_entry))
        folder_browse_button.pack()

        ctk.CTkLabel(edit_window, text="Toplam Dosya Sayısı:").pack()
        total_files_entry = ctk.CTkEntry(edit_window)
        total_files_entry.insert(0, str(selected_project.total_files))
        total_files_entry.pack()

        ctk.CTkLabel(edit_window, text="Bilgilendirme Mesajı:").pack()
        notification_message_entry = ctk.CTkEntry(edit_window)
        notification_message_entry.insert(0, selected_project.notification_message)
        notification_message_entry.pack()

        ctk.CTkLabel(edit_window, text="Ödeme Linki:").pack()
        payment_link_entry = ctk.CTkEntry(edit_window)
        payment_link_entry.insert(0, selected_project.payment_link)
        payment_link_entry.pack()

        ctk.CTkLabel(edit_window, text="Fiyat:").pack()
        price_entry = ctk.CTkEntry(edit_window)
        price_entry.insert(0,selected_project.price)
        price_entry.pack()

        ctk.CTkLabel(edit_window, text="GPU Sayısı:").pack()
        gpu_count_entry = ctk.CTkEntry(edit_window)
        gpu_count_entry.insert(0,selected_project.gpu_count)
        gpu_count_entry.pack()



        save_button = ctk.CTkButton(edit_window, text="Kaydet",
                                    command=lambda: self.update_project(edit_window, selected_project,
                                                                        project_name_entry, folder_path_entry,
                                                                        total_files_entry, notification_message_entry,
                                                                        payment_link_entry, gpu_count_entry, price_entry))
        save_button.pack(pady=10)

    def upload_selected_project(self,project_id):
        selected_project = next((project for project in self.projects if project.id == project_id), None)
        if selected_project is None:
            messagebox.showwarning("Hata", "Seçilen proje bulunamadı.")
            return

        selected_project.notification_message = "Upload ediliyor..."
        threading.Thread(target=self.perform_upload, args=(selected_project,)).start()

    def perform_upload(self, selected_project):
        upload_project(selected_project)


    def export_selected_project(self, project_id):
        selected_project = next((project for project in self.projects if project.id == project_id), None)
        if selected_project is None:
            messagebox.showwarning("Hata", "Seçilen proje bulunamadı.")
            return

        selected_project.notification_message = "Birleştiriliyor..."

        # Run export in a separate thread
        threading.Thread(target=self.perform_export, args=(selected_project,)).start()

    def perform_export(self, selected_project):
        # Perform the export process in a separate thread
        export_project(selected_project, self.update_export_status)

    def update_export_status(self, project_id):
        # Update export status on the main thread
        self.root.after(0, self._update_export_status, project_id)

    def _update_export_status(self, project_id):
        project = next((p for p in self.projects if p.id == project_id), None)
        if project:
            print(f"Project {project.name} marked as exported.")
            self.animation_frame.update_export_status(project_id, True)

    def update_project(self, window, project, name_entry, folder_entry, total_files_entry, message_entry, link_entry, gpu_count_entry,
                       price_entry):
        name = name_entry.get()
        folder_path = folder_entry.get()
        total_files = int(total_files_entry.get())
        notification_message = message_entry.get()
        payment_link = link_entry.get()
        gpu_count = gpu_count_entry.get()
        price = price_entry.get()

        if name and folder_path and total_files and notification_message:
            project.name = name
            project.folder_path = folder_path
            project.total_files = total_files
            project.notification_message = notification_message
            project.payment_link = payment_link
            project.gpu_count = gpu_count
            project.price = price

            if project.project_type == "Animation":

                for id, label in zip(self.animation_frame.id_list, self.animation_frame.label_list):
                    if id == project.id:
                        label.configure(text=name)
                        break
            else:
                for id, label in zip(self.render_frame.id_list, self.render_frame.label_list):
                    if id == project.id:
                        label.configure(text=name)
                        break

            window.destroy()
        else:
            messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun.")

    def remove_project(self, project_id):
        selected_project = next((project for project in self.projects if project.id == project_id), None)
        if selected_project is None:
            messagebox.showwarning("Hata", "Seçilen proje bulunamadı.")
            return

        selected_project.tracking = False

        data = {"project_id": selected_project.id}

        self.projects.remove(selected_project)

        if selected_project.project_type == "Animation":
            self.animation_frame.remove_item(project_id)
        else:
            self.render_frame.remove_item(project_id)

        try:
            response = requests.post(REMOVE_PROJECT_URL, json=data)
            response.raise_for_status()

            if response.status_code == 200:
                messagebox.showinfo("Bilgi", "Proje başarıyla silindi.")
            else:
                error_message = response.json().get('error', 'Unknown error')
                messagebox.showerror("Hata", f"Projeyi silerken hata oluştu: {error_message}")

        except requests.RequestException as e:
            messagebox.showerror("Hata", f"Sunucuya bağlanırken hata oluştu: {e}")

    @staticmethod
    def track_project(project, update_progress_callback):
        while project.tracking:
            try:
                current_files = len(os.listdir(project.folder_path))
                project.progress = (current_files / project.total_files) * 100
                data = {
                    "project_id":project.id,
                    "project_type":project.project_type,
                    "project_name": project.name,
                    "progress": project.progress,
                    "message": project.notification_message,
                    "price": project.price,
                    "payment_link": project.payment_link,
                    "gpu_count": project.gpu_count,
                    "framerate": project.fps,
                    "resolution": project.resolution
                }
                print(data)
                requests.post(ADD_PROJECT_URL, json=data)

                update_progress_callback(project.id, project.progress)

            except Exception as e:
                print(f"Hata: {e}")
            time.sleep(5)


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = ProjectTrackerApp(root)
    root.mainloop()
