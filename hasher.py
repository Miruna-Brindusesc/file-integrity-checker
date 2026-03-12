import hashlib
import os

def calculate_file_hash(file_path, algorithm="sha256"):
    """Calculate file hash with configurable algorithm"""
    try:
        hash_func = hashlib.new(algorithm)
        
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return None
            
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
    
    except Exception as e:
        print(f"Error hashing file: {e}")
        return None
