import json
import os
import shutil
from datetime import datetime

DB_FILE = "database.json"
BACKUP_DIR = "backups"

def load_database():
    """Load database with error handling"""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                content = f.read().strip()
                if not content:  # Empty file
                    return {}
                return json.loads(content)
        except json.JSONDecodeError:
            print("Warning: database.json is corrupted. Creating backup and new database.")
            backup_database()
            return {}           
    return {}

def save_database(db):
    """Save database with backup"""
    if os.path.exists(DB_FILE):
        backup_database()
    
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)
    print("Database saved successfully")

def backup_database():
    """Create a timestamped backup of the database"""
    if not os.path.exists(DB_FILE):
        return
    
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"database_backup_{timestamp}.json")
    
    shutil.copy2(DB_FILE, backup_file)
    print(f"Backup created: {backup_file}")