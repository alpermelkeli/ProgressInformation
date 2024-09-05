import customtkinter as ctk

from tkinter import filedialog, messagebox

import threading

import time

import os

from utils.Export import export_project
import requests

from component.ScrollableLabelButtonFrame import ScrollableLabelButtonFrame

from model.Project import Project

SERVER_URL = "http://example.com/post_data"


class ProjectTrackerApp:
    def __init__(self, root):
        self.root = root

        self.root.title("Project Tracker")

        self.projects = []

        self.projects_frame = ScrollableLabelButtonFrame(root, edit_command=self.edit_selected_project,
                                                         export_command=self.export_selected_project, remove_command=self.remove_project,width=500,
                                                         height=500)

        self.projects_frame.pack(pady=10)

        self.add_project_button = ctk.CTkButton(root, text="Yeni Proje Ekle", command=self.add_project)

        self.add_project_button.pack(pady=10)

    def add_project(self):
        new_project_window = ctk.CTkToplevel(self.root)
        new_project_window.title("Yeni Proje Ekle")

        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        new_project_window.geometry(f"{root_width}x{root_height}+{root_x}+{root_y}")

        new_project_window.focus_set()
        new_project_window.grab_set()

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

        add_button = ctk.CTkButton(new_project_window, text="Ekle",
                                   command=lambda: self.save_project(new_project_window, project_name_entry,
                                                                     folder_path_entry, total_files_entry,
                                                                     notification_message_entry, payment_link_entry,
                                                                     gpu_count_entry,price_entry))
        add_button.pack(pady=10)

    @staticmethod
    def browse_folder(entry):
        folder_path = filedialog.askdirectory()
        if folder_path:
            entry.delete(0, ctk.END)
            entry.insert(0, folder_path)

    def save_project(self, window, name_entry, folder_entry, total_files_entry, message_entry, link_entry,gpu_count_entry,price_entry):
        name = name_entry.get()
        folder_path = folder_entry.get()
        total_files = int(total_files_entry.get())
        notification_message = message_entry.get()
        payment_link = link_entry.get()
        gpu_count = gpu_count_entry.get()
        price = price_entry.get()
        if name and folder_path and total_files and notification_message and payment_link:
            new_project = Project(name, folder_path, total_files, notification_message, payment_link,gpu_count=gpu_count,price=price)
            self.projects.append(new_project)
            self.projects_frame.add_item(new_project.id, new_project.name)

            threading.Thread(target=self.track_project, args=(new_project, self.projects_frame.update_progress)).start()

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

        ctk.CTkLabel(edit_window, text="Dosya url'si:").pack()
        file_url_entry = ctk.CTkEntry(edit_window)
        file_url_entry.insert(0,selected_project.file_url)
        file_url_entry.pack()

        save_button = ctk.CTkButton(edit_window, text="Kaydet",
                                    command=lambda: self.update_project(edit_window, selected_project,
                                                                        project_name_entry, folder_path_entry,
                                                                        total_files_entry, notification_message_entry,
                                                                        payment_link_entry, gpu_count_entry,
                                                                        file_url_entry, price_entry))
        save_button.pack(pady=10)

    def export_selected_project(self, project_id):
        selected_project = next((project for project in self.projects if project.id == project_id), None)
        if selected_project is None:
            messagebox.showwarning("Hata", "Seçilen proje bulunamadı.")
            return

        export_window = ctk.CTkToplevel(self.root)
        export_window.title("Projeyi Export Et")

        # Set window position and size
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        export_window.geometry(f"{root_width}x{root_height}+{root_x}+{root_y}")
        export_window.focus_set()
        export_window.grab_set()

        # FPS Selection
        ctk.CTkLabel(export_window, text="fps:").pack()
        fps_option_menu = ctk.CTkOptionMenu(export_window, values=["1", "25", "30", "60", "200"])
        fps_option_menu.pack()

        # Output Name
        ctk.CTkLabel(export_window, text="output adı:").pack()
        output_name_entry = ctk.CTkEntry(export_window)
        output_name_entry.insert(0, "output.mp4")
        output_name_entry.pack()

        # File Type
        ctk.CTkLabel(export_window, text="dosya türü:").pack()
        file_type_entry = ctk.CTkEntry(export_window)
        file_type_entry.insert(0, "tga")
        file_type_entry.pack()

        # Resolution Selection
        resolution_option_menu = ctk.CTkOptionMenu(export_window, values=["640x360", "1280x720", "1920x1080", "2560x1440", "3840x2160"])
        resolution_option_menu.pack()

        # Export Button with callback
        export_button = ctk.CTkButton(export_window, text="Kaydet",
                                      command=lambda: export_project(
                                          selected_project, selected_project.folder_path, fps_option_menu.get(),
                                          output_name_entry.get(), file_type_entry.get(), resolution_option_menu.get(),
                                          self.update_export_status  # Pass the callback function
                                      ))
        export_button.pack(pady=10)

    def update_export_status(self, project_id):
        project = next((p for p in self.projects if p.id == project_id), None)
        if project:
            print(f"Project {project.name} marked as exported.")
            self.projects_frame.update_export_status(project_id,
                                              True)

    def update_project(self, window, project, name_entry, folder_entry, total_files_entry, message_entry, link_entry, gpu_count_entry,
                       file_url_entry,price_entry):
        name = name_entry.get()
        folder_path = folder_entry.get()
        total_files = int(total_files_entry.get())
        notification_message = message_entry.get()
        payment_link = link_entry.get()
        gpu_count = gpu_count_entry.get()
        file_url = file_url_entry.get()
        price = price_entry.get()

        if name and folder_path and total_files and notification_message and payment_link:
            project.name = name
            project.folder_path = folder_path
            project.total_files = total_files
            project.notification_message = notification_message
            project.payment_link = payment_link
            project.gpu_count = gpu_count
            project.file_url = file_url
            project.price = price

            for id, label in zip(self.projects_frame.id_list, self.projects_frame.label_list):
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

        # Stop tracking by setting the flag to False
        selected_project.tracking = False

        # Remove the project from the list and UI
        self.projects.remove(selected_project)
        self.projects_frame.remove_item(project_id)

        messagebox.showinfo("Bilgi", "Proje başarıyla silindi.")

    @staticmethod
    def track_project(project, update_progress_callback):
        while project.tracking:
            try:
                current_files = len(os.listdir(project.folder_path))
                project.progress = (current_files / project.total_files) * 100
                data = {
                    "project_name": project.name,
                    "progress": project.progress,
                    "message": project.notification_message,
                    "price": project.price,
                    "payment_link": project.payment_link,
                    "file_url": project.file_url,
                    "gpu_count": project.gpu_count
                }
                print(data)
                requests.post(SERVER_URL, json=data)

                update_progress_callback(project.id, project.progress)

            except Exception as e:
                print(f"Hata: {e}")
            time.sleep(5)


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")  # Temayı ayarla
    ctk.set_default_color_theme("blue")  # Renk temasını ayarla
    root = ctk.CTk()
    app = ProjectTrackerApp(root)
    root.mainloop()
