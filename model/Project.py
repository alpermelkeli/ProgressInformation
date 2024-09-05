
class Project:
    def __init__(self, name, folder_path, total_files, notification_message, payment_link, gpu_count,file_url=""):
        self.id = id(self)  # Assuming this is how IDs are generated
        self.name = name
        self.folder_path = folder_path
        self.total_files = total_files
        self.notification_message = notification_message
        self.payment_link = payment_link
        self.gpu_count = gpu_count
        self.progress = 0
        self.file_url = file_url
        self.tracking = True  # New flag to control tracking
