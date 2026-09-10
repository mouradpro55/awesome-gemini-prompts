from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TabbedContent, TabPane

from ui.screens import PingTab, SocketTab, SerialTab, SnifferTab

class NetTUIApp(App):
    """A Textual app for Network and Telemetry diagnostics."""

    CSS_PATH = "ui/styles.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(initial="ping_tab"):
            with TabPane("Ping", id="ping_tab"):
                yield PingTab()
            with TabPane("Socket Diagnostics", id="socket_tab"):
                yield SocketTab()
            with TabPane("Serial Monitor", id="serial_tab"):
                yield SerialTab()
            with TabPane("Packet Sniffer", id="sniffer_tab"):
                yield SnifferTab()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

if __name__ == "__main__":
    app = NetTUIApp()
    app.run()
