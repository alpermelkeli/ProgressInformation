import uuid

class Project:
    def __init__(self, name, folder_path, total_files, notification_message, payment_link, file_url=""):
        self.id = str(uuid.uuid4())  # Benzersiz bir ID oluştur
        self.name = name
        self.folder_path = folder_path
        self.total_files = total_files
        self.notification_message = notification_message
        self.payment_link = payment_link
        self.progress = 0
        self.file_url = file_url
