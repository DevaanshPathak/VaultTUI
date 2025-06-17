# 🔐 VaultTUI - Encrypted CLI Password Manager

VaultTUI is a secure, command-line-based password manager built in Python. It uses AES encryption (via Fernet) to protect your data and offers a text-based UI and CLI interface for managing credentials locally — offline, encrypted, and private.

---

## ✅ Day 1 Progress (CLI Interface)

### 🚀 Features Implemented

#### 1. Master Password Management
- 🔐 Password-protected access to the vault
- Password hashing with SHA-256
- First-time password setup and password change functionality
- Vault data is re-encrypted when password changes

#### 2. CLI Commands via `argparse`
All commands prompt for the master password and provide user-friendly output:
```bash
python vault.py [command] [args...]
````

#### Available Commands:

| Command        | Description                       |
| -------------- | --------------------------------- |
| `add`          | Add a new entry                   |
| `get` / `view` | View an entry by name             |
| `delete`       | Delete an entry                   |
| `list`         | List all entries                  |
| `search`       | Search entries by keyword         |
| `edit`         | Edit an existing entry            |
| `backup`       | Backup the encrypted vault        |
| `restore`      | Restore the most recent backup    |
| `set-password` | Set or change the master password |

#### Example:

```bash
python vault.py add github user123 pass123
python vault.py get github
python vault.py search git
python vault.py delete github
```

---

## 🗄️ Vault Storage

* Data is stored in an encrypted JSON format using `cryptography.fernet`
* Only the correct master password can decrypt the vault

---

## 💾 Backup & Restore

* `backup_vault()` automatically saves timestamped backups of your vault
* `restore_vault()` restores the latest backup if available

---

## 📁 Project Structure

```
VaultTUI/
│
├── vault.py             # CLI interface using argparse
├── utils.py             # Encryption, decryption, vault IO, password logic
├── config.py            # File paths (vault file, backups, etc.)
├── vault_data.enc       # Encrypted vault file (auto-created)
├── backups/             # Stores timestamped vault backups
└── .vault_pass          # Stores hashed master password (SHA-256)
```

---

## 🧠 Concepts Used

* 🔐 Fernet symmetric encryption (AES-128 under the hood)
* 🧂 PBKDF2 key derivation with a salt
* 🧵 CLI design with `argparse`
* 💾 Safe file operations for backup/restore
* 📂 Tidy code structure with separation of concerns

---

## 📅 Day 2 Goals (Next Steps)

* Implement Textual-based TUI (Text User Interface)
* Add clipboard copy feature
* Optional: Restore from a selected backup
* Optional: Export vault to plaintext for recovery

---

## 👤 Author

Devaansh Pathak
