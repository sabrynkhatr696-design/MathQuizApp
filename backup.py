from datetime import datetime
import os
import shutil

# المتغيرات
current_day = datetime.now().strftime('%Y-%m-%d')
backup_path = os.path.join(os.getcwd(), "Backups")  # مجلد Backups في نفس المشروع
no_tables = 10
file_size = 5000
backup_size = []
total_size = 10000

# إنشاء مجلد Backups إذا مش موجود
if not os.path.exists(backup_path):
    os.mkdir(backup_path)

# دالة النسخ الاحتياطي
def backup():
    db_file = "global.db"
    dest_folder = os.path.join(backup_path, current_day)
    os.makedirs(dest_folder, exist_ok=True)
    shutil.copy2(db_file, dest_folder)
    print(f"Backup completed for {db_file} to {dest_folder}")

# منطق النسخ الاحتياطي
current_day_folder = os.path.join(backup_path, current_day)
if os.path.exists(current_day_folder):
    files = os.listdir(current_day_folder)
    if len(files) < no_tables or sum(os.stat(os.path.join(current_day_folder, f)).st_size for f in files) < total_size:
        shutil.rmtree(current_day_folder)
        backup()
else:
    backup()