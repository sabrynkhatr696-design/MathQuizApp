import os
import shutil
from datetime import datetime


def backup_db():
    db_file = "global.db"
    backup_path = os.path.join(os.getcwd(), "Backups")
    os.makedirs(backup_path, exist_ok=True)

    current_day = datetime.now().strftime("%Y-%m-%d")
    dest_folder = os.path.join(backup_path, current_day)
    os.makedirs(dest_folder, exist_ok=True)

    shutil.copy2(db_file, dest_folder)
    print(f"Backup completed for {db_file} to {dest_folder} ✅")