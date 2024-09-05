# In model/Project.py

class Project:
    def __init__(self, name, folder_path, total_files,notification_message, payment_link, gpu_count,  price = "0", project_type= "Animation"):
        self.id = id(self)  # Unique identifier for the project
        self.name = name
        self.folder_path = folder_path
        self.total_files = total_files
        self.notification_message = notification_message
        self.payment_link = payment_link
        self.gpu_count = gpu_count
        self.price = price
        self.progress = 0,
        self.project_type = project_type
        self.tracking = True
        self.exported = False  # New attribute to track export status
