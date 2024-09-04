import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading

import time

import os

import requests

from component.ScrollableLabelButtonFrame import ScrollableLabelButtonFrame

from model.Project import Project

SERVER_URL = "http://example.com/post_data"

class ProjectTrackerApp:
    def __init__(self, root):
        self.root = root

        self.root.title("Project Tracker")

        self.projects = []

        # Mevcut projeler bölümü
        self.projects_frame = ScrollableLabelButtonFrame(root, command=self.edit_selected_project, width=500, height=300)

        self.projects_frame.pack(pady=10)

        # Yeni proje ekleme bölümü
        self.add_project_button = ctk.CTkButton(root, text="Yeni Proje Ekle", command=self.add_project)

        self.add_project_button.pack(pady=10)

    def add_project(self):
        new_project_window = ctk.CTkToplevel(self.root)
        new_project_window.title("Yeni Proje Ekle")

        # Root penceresinin boyutlarını ve konumunu alın
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        # Yeni pencereyi root'un üzerine yerleştirin
        new_project_window.geometry(f"{root_width}x{root_height}+{root_x}+{root_y}")

        # Pencereyi ön plana getir ve kullanıcıyı pencereyle etkileşime zorla
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

        add_button = ctk.CTkButton(new_project_window, text="Ekle",
                                   command=lambda: self.save_project(new_project_window, project_name_entry,
                                                                     folder_path_entry, total_files_entry,
                                                                     notification_message_entry, payment_link_entry))
        add_button.pack(pady=10)
    def browse_folder(self, entry):
        folder_path = filedialog.askdirectory()
        if folder_path:
            entry.delete(0, ctk.END)
            entry.insert(0, folder_path)

    def save_project(self, window, name_entry, folder_entry, total_files_entry, message_entry, link_entry):
        name = name_entry.get()
        folder_path = folder_entry.get()
        total_files = int(total_files_entry.get())
        notification_message = message_entry.get()
        payment_link = link_entry.get()

        if name and folder_path and total_files and notification_message and payment_link:
            new_project = Project(name, folder_path, total_files, notification_message, payment_link)
            self.projects.append(new_project)
            self.projects_frame.add_item(name)

            threading.Thread(target=self.track_project, args=(new_project, self.projects_frame.update_progress)).start()

            window.destroy()
        else:
            messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun.")

    def edit_selected_project(self, project_name):
        selected_project = next((project for project in self.projects if project.name == project_name), None)
        if selected_project is None:
            messagebox.showwarning("Hata", "Seçilen proje bulunamadı.")
            return

        edit_window = ctk.CTkToplevel(self.root)
        edit_window.title("Projeyi Düzenle")

        # Root penceresinin boyutlarını ve konumunu alın
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        # Edit window'u root'un üzerine yerleştirin
        edit_window.geometry(f"{root_width}x{root_height}+{root_x}+{root_y}")

        # Pencereyi ön plana getir ve kullanıcıyı pencereyle etkileşime zorla
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

        save_button = ctk.CTkButton(edit_window, text="Kaydet",
                                    command=lambda: self.update_project(edit_window, selected_project,
                                                                        project_name_entry, folder_path_entry,
                                                                        total_files_entry, notification_message_entry,
                                                                        payment_link_entry))
        save_button.pack(pady=10)

    def update_project(self, window, project, name_entry, folder_entry, total_files_entry, message_entry, link_entry):
        name = name_entry.get()
        folder_path = folder_entry.get()
        total_files = int(total_files_entry.get())
        notification_message = message_entry.get()
        payment_link = link_entry.get()

        if name and folder_path and total_files and notification_message and payment_link:
            project.name = name
            project.folder_path = folder_path
            project.total_files = total_files
            project.notification_message = notification_message
            project.payment_link = payment_link

            self.projects_frame.remove_item(name)
            self.projects_frame.add_item(name)

            window.destroy()
        else:
            messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun.")

    @staticmethod
    def track_project(project, update_progress_callback):
        while True:
            try:
                current_files = len(os.listdir(project.folder_path))
                project.progress = (current_files / project.total_files) * 100
                data = {
                    "project_name": project.name,
                    "progress": project.progress,
                    "message": project.notification_message,
                    "payment_link": project.payment_link
                }
                print(data)
                requests.post(SERVER_URL, json=data)

                # Progress'ı GUI üzerinde güncelle
                update_progress_callback(project.name, project.progress)

            except Exception as e:
                print(f"Hata: {e}")
            time.sleep(60)


if __name__ == "__main__":

    ctk.set_appearance_mode("Dark")  # Temayı ayarla
    ctk.set_default_color_theme("blue")  # Renk temasını ayarla

    root = ctk.CTk()
    app = ProjectTrackerApp(root)
    root.mainloop()
