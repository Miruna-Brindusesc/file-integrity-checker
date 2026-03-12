from hasher import calculate_file_hash
from utils import load_database, save_database
import os
import sys

try:
    from colorama import init, Fore, Style
    init()
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class Fore:
        RED = GREEN = YELLOW = BLUE = WHITE = ''
    class Style:
        RESET_ALL = ''

def print_color(message, color=Fore.WHITE):
    """Print with color if available"""
    if HAS_COLOR:
        print(f"{color}{message}{Style.RESET_ALL}")
    else:
        print(message)

def add_file(filepath):
    """Add a file to monitoring"""
    db = load_database()

    if not os.path.exists(filepath):
        print_color(f"Error: File '{filepath}' doesn't exist", Fore.RED)
        return

    file_size = os.path.getsize(filepath)
    modified_time = os.path.getmtime(filepath)
    
    file_hash = calculate_file_hash(filepath)
    
    if file_hash is None:
        print_color("Failed to calculate file hash", Fore.RED)
        return

    db[filepath] = {
        "hash": file_hash,
        "size": file_size,
        "modified": modified_time,
        "added": __import__('time').time()
    }
    
    save_database(db)
    print_color(f" File added to monitoring: {filepath}", Fore.GREEN)
    print_color(f"  Size: {file_size} bytes", Fore.BLUE)
    print_color(f"  Hash: {file_hash[:16]}...", Fore.BLUE)

def verify_files():
    """Verify all monitored files"""
    db = load_database()
    
    if not db:
        print_color("No files in database. Add some files first!", Fore.YELLOW)
        return
    
    print_color("\n" + "="*50, Fore.WHITE)
    print_color("VERIFYING FILE INTEGRITY", Fore.WHITE)
    print_color("="*50, Fore.WHITE)
    
    modified_count = 0
    missing_count = 0
    ok_count = 0
    
    for filepath, file_info in db.items():
        if isinstance(file_info, str):
            stored_hash = file_info
        else:
            stored_hash = file_info.get("hash", "")
        
        if not os.path.exists(filepath):
            print_color(f"[MISSING] {filepath}", Fore.YELLOW)
            missing_count += 1
            continue
            
        current_hash = calculate_file_hash(filepath)
        
        if current_hash != stored_hash:
            print_color(f"[MODIFIED] {filepath}", Fore.RED)
            modified_count += 1
        else:
            print_color(f"[OK] {filepath}", Fore.GREEN)
            ok_count += 1
    
    print_color("\n" + "="*50, Fore.WHITE)
    print_color("SUMMARY", Fore.WHITE)
    print_color(f"OK: {ok_count}", Fore.GREEN)
    print_color(f"Modified: {modified_count}", Fore.RED)
    print_color(f"Missing: {missing_count}", Fore.YELLOW)
    print_color("="*50, Fore.WHITE)

def main():
    """Main menu"""
    while True:
        print_color("\n" + "="*40, Fore.BLUE)
        print_color("FILE INTEGRITY MONITOR", Fore.BLUE)
        print_color("="*40, Fore.BLUE)
        print_color("1. Add file to monitoring", Fore.WHITE)
        print_color("2. Verify all files", Fore.WHITE)
        print_color("3. Exit", Fore.WHITE)
        print_color("="*40, Fore.BLUE)
        
        choice = input("Select option (1-3): ").strip()
        
        if choice == "1":
            path = input("Enter file path: ").strip()
            add_file(path)
        elif choice == "2":
            verify_files()
        elif choice == "3":
            print_color("Goodbye!", Fore.GREEN)
            break
        else:
            print_color("Invalid option. Please try again.", Fore.RED)
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_color("\n\nProgram interrupted. Goodbye!", Fore.YELLOW)
        sys.exit(0)