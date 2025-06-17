from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, Button, Static, Input, Label
from textual.message import Message
import getpass
from vault import delete_entry, search_entries
from utils import (
    load_vault,
    save_vault,
    generate_key,
    validate_master_password,
    get_entry,
    delete_entry_manual,
    search_entries_manual,
)


class Sidebar(Vertical):
    def compose(self) -> ComposeResult:
        yield Static("🔐 VaultTUI", classes="title")
        yield Button("➕ Add", id="add")
        yield Button("👁️ View", id="view")
        yield Button("🗑️ Delete", id="delete")
        yield Button("🔍 Search", id="search")


class AddEntryForm(Container):
    class Submit(Message):
        def __init__(self, sender, name, username, password) -> None:
            super().__init__()
            self.sender = sender
            self.name = name
            self.username = username
            self.password = password

    def compose(self) -> ComposeResult:
        yield Label("🔐 Add New Entry", id="form-title")
        yield Input(placeholder="Entry name", id="entry-name")
        yield Input(placeholder="Username", id="entry-username")
        yield Input(placeholder="Password", password=True, id="entry-password")
        yield Button("✅ Save", id="submit")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            name = self.query_one("#entry-name", Input).value
            username = self.query_one("#entry-username", Input).value
            password = self.query_one("#entry-password", Input).value
            self.post_message(self.Submit(self, name, username, password))

class VaultApp(App):
    CSS_PATH = "tui.css"

    def __init__(self, key: bytes):
        super().__init__()
        self.key = key

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Sidebar(id="sidebar"),
            Container(id="main-content"),
            id="main"
        )
        yield Footer()

    def on_mount(self):
        self.show_welcome()

    def show_welcome(self):
        self.query_one("#main-content", Container).remove_children()
        self.query_one("#main-content", Container).mount(Static("👋 Welcome to VaultTUI!", id="welcome-msg"))

    def show_add_form(self):
        self.query_one("#main-content", Container).remove_children()
        self.query_one("#main-content", Container).mount(AddEntryForm())

    def show_view_form(self):
        self.query_one("#main-content", Container).remove_children()
        self.query_one("#main-content", Container).mount(
            Input(placeholder="Enter entry name", id="view-name"),
            Button("👁️ View", id="view-submit")
        )

    def show_delete_form(self):
        self.query_one("#main-content", Container).remove_children()
        self.query_one("#main-content", Container).mount(
            Input(placeholder="Enter entry name", id="delete-name"),
            Button("🗑️ Delete", id="delete-submit")
        )

    def show_search_form(self):
        self.query_one("#main-content", Container).remove_children()
        self.query_one("#main-content", Container).mount(
            Input(placeholder="Search keyword", id="search-keyword"),
            Button("🔍 Search", id="search-submit")
        )

    def on_button_pressed(self, event: Button.Pressed):
        btn_id = event.button.id
        if btn_id == "add":
            self.show_add_form()
        elif btn_id == "view":
            self.show_view_form()
        elif btn_id == "delete":
            self.show_delete_form()
        elif btn_id == "search":
            self.show_search_form()
        elif btn_id == "view-submit":
            name = self.query_one("#view-name", Input).value
            vault = load_vault(self.key)
            try:
                vault = load_vault(self.key)
                entry = vault.get(name)
                self.query_one("#main-content", Container).remove_children()
                self.query_one("#main-content", Container).mount(
                    Static(f"🔐 {name}:\nUsername: {entry['username']}\nPassword: {entry['password']}")
                )
            except KeyError:
                self.query_one("#main-content", Container).mount(Static(f"❌ Entry '{name}' not found."))
        elif btn_id == "delete-submit":
            name = self.query_one("#delete-name", Input).value
            vault = load_vault(self.key)
            try:
                success = delete_entry_manual(name, vault)
                if success:
                    save_vault(vault, self.key)
                    self.query_one("#main-content", Container).remove_children()
                    self.query_one("#main-content", Container).mount(
                        Static(f"🗑️ Entry '{name}' deleted.")
                    )
                else:
                    self.query_one("#main-content", Container).remove_children()
                    self.query_one("#main-content", Container).mount(
                        Static(f"❌ Entry '{name}' not found.")
                    )

                save_vault(vault, self.key)
                self.query_one("#main-content", Container).remove_children()
                self.query_one("#main-content", Container).mount(Static(f"🗑️ Entry '{name}' deleted."))
            except KeyError:
                self.query_one("#main-content", Container).mount(Static(f"❌ Entry '{name}' not found."))
        elif btn_id == "search-submit":
            keyword = self.query_one("#search-keyword", Input).value
            vault = load_vault(self.key)
            results = search_entries_manual(keyword, vault)
            self.query_one("#main-content", Container).remove_children()
            if results:
                output = "\n".join(f"🔹 {k}: {v['username']}" for k, v in results.items())
                self.query_one("#main-content", Container).mount(Static(f"🔍 Search results:\n{output}"))
            else:
                self.query_one("#main-content", Container).mount(Static("❌ No matching entries found."))

    def on_add_entry_form_submit(self, msg: AddEntryForm.Submit):
        vault = load_vault(self.key)
        if msg.name in vault:
            self.query_one("#main-content", Container).mount(Static(f"⚠️ Entry '{msg.name}' already exists."))
        else:
            vault[msg.name] = {
                "username": msg.username,
                "password": msg.password
            }
            save_vault(vault, self.key)
            self.query_one("#main-content", Container).remove_children()
            self.query_one("#main-content", Container).mount(Static(f"✅ Entry '{msg.name}' added!"))


def main():
    pw = getpass.getpass("Enter master password: ")
    if not validate_master_password(pw):
        print("❌ Incorrect master password.")
        return
    key = generate_key(pw)
    app = VaultApp(key)
    app.run()


if __name__ == "__main__":
    main()
