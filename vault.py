import argparse
import getpass
import config
from config import VAULT_FILE, VAULT_DIR

from utils import (
    generate_key,
    encrypt,
    decrypt,
    load_vault,
    save_vault,
    backup_vault,
    restore_vault,
    set_master_password_securely,
    validate_master_password,
)
from config import VAULT_FILE

def prompt_password():
    return getpass.getpass("Enter master password: ")

def add_entry(args):
    password = prompt_password()
    key = generate_key(password)
    vault = load_vault(key)

    if args.name in vault:
        print(f"❗ Entry '{args.name}' already exists.")
        return

    vault[args.name] = {
        "username": args.username,
        "password": args.password,
    }
    save_vault(vault, key)
    print(f"✅ Entry '{args.name}' added.")

def view_entry(args):
    password = prompt_password()
    key = generate_key(password)
    vault = load_vault(key)

    if args.name not in vault:
        print(f"❌ Entry '{args.name}' not found.")
        return

    entry = vault[args.name]
    print(f"🔐 {args.name}:")
    print(f"   Username: {entry['username']}")
    print(f"   Password: {entry['password']}")

def delete_entry(args):
    password = prompt_password()
    key = generate_key(password)
    vault = load_vault(key)

    if args.name not in vault:
        print(f"❌ Entry '{args.name}' not found.")
        return

    del vault[args.name]
    save_vault(vault, key)
    print(f"🗑️ Entry '{args.name}' deleted.")

def list_entries(args):
    password = prompt_password()
    key = generate_key(password)
    vault = load_vault(key)

    print("📁 Saved entries:")
    for name in vault:
        print(f"- {name}")

def search_entries(args):
    password = prompt_password()
    key = generate_key(password)
    vault = load_vault(key)

    print(f"🔍 Search results for '{args.query}':")
    for name in vault:
        if args.query.lower() in name.lower():
            print(f"- {name}")

def handle_backup(args):
    backup_vault()
    print("🗃️ Backup created.")

def handle_restore(args):
    restore_vault()
    print("📦 Vault restored from backup.")

def handle_set_password(args):
    old_pw = getpass.getpass("Enter current master password: ")
    new_pw = getpass.getpass("Enter new master password: ")
    confirm_pw = getpass.getpass("Confirm new master password: ")

    if new_pw != confirm_pw:
        print("❌ Passwords do not match.")
        return

    set_master_password_securely(old_pw, new_pw)


# CLI Setup
parser = argparse.ArgumentParser(description="🔐 VaultTUI - Encrypted CLI Password Manager")
subparsers = parser.add_subparsers(dest="command", required=True)

# Add
add_parser = subparsers.add_parser("add", help="Add a new entry")
add_parser.add_argument("name", help="Entry name (e.g., github)")
add_parser.add_argument("username", help="Username or email")
add_parser.add_argument("password", help="Password")
add_parser.set_defaults(func=add_entry)

# View
view_parser = subparsers.add_parser("view", help="View an entry")
view_parser.add_argument("name", help="Entry name")
view_parser.set_defaults(func=view_entry)

# Delete
delete_parser = subparsers.add_parser("delete", help="Delete an entry")
delete_parser.add_argument("name", help="Entry name")
delete_parser.set_defaults(func=delete_entry)

# List
list_parser = subparsers.add_parser("list", help="List all entries")
list_parser.set_defaults(func=list_entries)

# Search
search_parser = subparsers.add_parser("search", help="Search entries")
search_parser.add_argument("query", help="Search query")
search_parser.set_defaults(func=search_entries)

# Backup
backup_parser = subparsers.add_parser("backup", help="Backup the vault")
backup_parser.set_defaults(func=handle_backup)

# Restore
restore_parser = subparsers.add_parser("restore", help="Restore from backup")
restore_parser.set_defaults(func=handle_restore)

# Set/Change password
setpass_parser = subparsers.add_parser("set-password", help="Set or change master password")
setpass_parser.add_argument("new_password", help="New master password")
setpass_parser.set_defaults(func=handle_set_password)

# Run
args = parser.parse_args()
args.func(args)
