# SnortAMV - Automated Snort Manager

A Python-based CLI tool to manage Snort Network Intrusion Detection System (IDS) with automated configuration, rule management, and user account handling.

## Features

- ✅ **Account Management** - Create, update, delete project users
- ✅ **Rule Management** - Add and list custom Snort detection rules
- ✅ **Configuration Validation** - Validate Snort config files
- ✅ **Cross-platform** - Supports Windows and Linux
- ✅ **Traffic Decryption** - Decrypt TLS-encrypted network traffic logs using SSL keys

## Installation

### Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **Snort** or **Snort3** (installed separately via `post_installer.py`)

### Quick Start

1. **Clone or navigate to the project directory:**
   ```bash
   cd SnortAMV
   ```
1.1 **Creating and Activating the Environment:**
##### Create & activate a virtual environment (recommended)

##### Why?
###### To isolate dependencies and avoid conflicts with your system Python.

   **To Create the environment**
   ```python
   python -m venv env
   ```
   **Activating the environment:**
   **For Windows**
   ```powershell 
   env\Scripts\Activate.ps1
   ```
   ```cmd
   env\Scripts\activate
   ```
   **For linux and macOS**
   ```bash
   source/env/bin/activate
   ```
2. **Install the package and dependencies:**
   ```bash
   pip install -e .
   ```
   This will:
   - Install all Python dependencies from `requirements.txt` (Windows) or `linux_requirements.txt` (Linux)
   - Create a `snortamv` command
   - Automatically run `post_installer.py` to install Snort and system dependencies

3. **Initialize your project:**
   ```bash
   snortamv setup
   ```
   This checks if Snort is installed and creates default detection rules.

4. **Verify installation:**
   ```bash
   snortamv --version
   ```

## Usage

### Help
```bash
snortamv -h
```

### Setup
```bash
snortamv setup
```

### Rule Management
```bash
snortamv rule add      # Add a custom detection rule interactively
snortamv rule list     # Display all local rules
```

### Account Management
```bash
snortamv acc create     # Create a project user
snortamv acc delete     # Delete a user
snortamv acc update     # Update user details
```

### Configuration
```bash
snortamv validate   # Validate Snort configuration
```

### Run Snort
```bash
snortamv run
```

### Traffic Decryption
```bash
  snortamv decrypt # for both (Linux) and (windows powershell) 
```

## Project Structure

```
SnortAMV/
├── main.py                     # Entry point
├── setup.py                    # Package configuration
├── requirements.txt            # Python dependencies (Windows)
├── linux_requirements.txt       # Python dependencies (Linux)
├── post_installer.py           # System setup (installs Snort, etc.)
├── database/
│   └── db.py                   # User account & data persistence
├── modules/
│   ├── acc_managt/             # Account management
│   ├── configuration/          # Rule & config management
│   └── utilities/              # Helper functions
├── rules/
│   └── local.rules             # Custom Snort detection rules
├── templates/
│   └── snort.conf.tpl          # Snort configuration template
├── decrypt.bash                # Linux traffic decryption script
├── decrypt.ps1                 # Windows traffic decryption script
└── snort.ps1 / snort_auto.bash # Run Snort on each platform
```

## Important Notes

### ⚠️ Do NOT run `pip freeze`

**Never** use `pip freeze > requirements.txt` on this project. It will:
- Overwrite the carefully maintained requirements files
- Break installations on other platforms (Windows/Linux)
- Create version conflicts

If you need to update dependencies:
1. Edit `requirements.txt` (Windows) or `linux_requirements.txt` (Linux) directly
2. Test on the appropriate platform
3. Commit changes to version control

### Database

- **Windows**: User database stored in `C:\Users\{username}\Desktop\SnortAMV\sqlite.db`
- **Linux**: User database stored in project directory as `sqlite.db`

The database is auto-initialized on first run.

### Configuration Files

- `snort.conf` - Main Snort IDS configuration
- `rules/local.rules` - Custom detection rules (created during setup)

## Troubleshooting

### Snort not found
```
[!] Snort not found. Please run post_installer.py first.
```
**Fix:** Run `pip install -e .` to trigger `post_installer.py`, or manually run:
```bash
python post_installer.py
```

### Database errors
If the SQLite database is corrupted, delete `sqlite.db` and re-run:
```bash
snortamv setup
```

### Import errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt      # Windows
pip install -r linux_requirements.txt # Linux
```

## Development

To install in editable mode for development:
```bash
pip install -e .
```

## License

Developed by Francis David

## Support

For issues or questions, refer to the documentation or check the source code comments.
