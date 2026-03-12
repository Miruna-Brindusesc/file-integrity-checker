# File Integrity Monitor

A lightweight Python tool that monitors files and detects modifications using cryptographic hashes (SHA-256). The program stores file hashes in a local JSON database and verifies whether any monitored file has been changed.

## Current Features

- **Add files to monitoring** - Calculate and store SHA-256 hashes of files
- **Verify file integrity** - Check if monitored files have been modified
- **File metadata tracking** - Stores file size and modification time
- **Automatic database backups** - Creates backups before modifying the database
- **Missing file detection** - Identifies when monitored files are no longer present
- **Colored console output** - Easy-to-read status indicators (green for OK, red for modified, yellow for missing)
- **Summary statistics** - Shows counts of OK, modified, and missing files after verification
- **Graceful shutdown** - Handles Ctrl+C interrupts properly

## Requirements

- Python 3.x 
- colorama (for colored output)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/file-integrity-monitor.git
   cd file-integrity-monitor
   ```

2. Create and activate a virtual environment:

   **Linux / Mac:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python src/monitor.py
```

### Main Menu

```
========================================
FILE INTEGRITY MONITOR
========================================
1. Add file to monitoring
2. Verify all files
3. Exit
========================================
Select option (1-3):
```

### Adding a File

Select option 1 and enter the file path:
```
Select option (1-3): 1
Enter file path: requirements.txt
  File added to monitoring: requirements.txt
  Size: 49 bytes
  Hash: 0b901940fe6799ab...

Press Enter to continue...
```

### Verifying Files

Select option 2 to check all monitored files:
```
Select option (1-3): 2

==================================================
VERIFYING FILE INTEGRITY
==================================================
[OK] requirements.txt

==================================================
SUMMARY
OK: 1
Modified: 0
Missing: 0
==================================================

Press Enter to continue...
```

### Example Output Scenarios

**When a file is modified:**
```
[MODIFIED] config.txt
```

**When a file is missing:**
```
[MISSING] important.doc
```

**When multiple files are checked:**
```
==================================================
VERIFYING FILE INTEGRITY
==================================================
[OK] requirements.txt
[OK] src/hasher.py
[MODIFIED] src/utils.py
[OK] README.md
[MISSING] old_config.bak

==================================================
SUMMARY
OK: 3
Modified: 1
Missing: 1
==================================================
```

## Project Structure

```
file-integrity-monitor/
│
├── src/
│   ├── monitor.py          # Main application with menu system
│   ├── hasher.py           # SHA-256 hash calculation
│   └── utils.py            # Database management utilities
│
├── requirements.txt         # Python dependencies (colorama)
├── database.json            # File hash database (auto-generated)
├── backups/                 # Database backups (auto-created)
└── README.md                # This file
```

## File Descriptions

| File | Description |
|------|-------------|
| `src/monitor.py` | Contains the main menu loop and core functions (add_file, verify_files) |
| `src/hasher.py` | Handles cryptographic hash calculation using SHA-256 |
| `src/utils.py` | Manages JSON database loading, saving, and backups |
| `database.json` | Stores file paths and their corresponding hashes with metadata |
| `backups/` | Directory containing timestamped backups of database.json |

## Database Format

The `database.json` file stores file information in the following format:

```json
{
  "/path/to/file.txt": {
    "hash": "sha256_hash_value_here",
    "size": 1024,
    "modified": 1234567890.123,
    "added": 1234567890.456
  }
}
```

## How It Works

1. **Adding a file**: The program calculates the SHA-256 hash of the file and stores it along with metadata (size, modification time) in database.json
2. **Verifying files**: The program recalculates the hash of each monitored file and compares it with the stored value
3. **Change detection**: If the hash differs, the file has been modified. If the file is missing, it's reported as missing
4. **Backups**: Before any database modification, a timestamped backup is created in the backups folder

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "database.json is corrupted" warning | The program automatically creates backups. Restore from the most recent file in the `/backups` directory. |
| File not found during verification | Files are marked as [MISSING] in the output. Use option 1 to re-add them if they've been moved. |
| Permission denied when accessing files | Ensure you have read permissions for all monitored files. |
| Colors not showing in terminal | Install colorama: `pip install colorama` or check your terminal supports ANSI colors |

## requirements.txt

```
colorama>=0.4.6
```
