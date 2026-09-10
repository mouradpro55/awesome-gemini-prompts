from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Header, Footer, Button, Input, Select, Log, Label, TabbedContent, TabPane
from textual.worker import Worker, WorkerState
import asyncio

from core.ping_runner import PingRunner
from core.socket_client import SocketClient
from core.serial_reader import SerialReader
from core.sniffer import PacketSniffer

class PingTab(Container):
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Input(placeholder="Host (e.g. 8.8.8.8)", id="ping_host", value="8.8.8.8"),
            Input(placeholder="Count", id="ping_count", value="4", type="integer"),
            Button("Ping", id="btn_ping", variant="primary"),
            id="ping_controls"
        )
        yield Log(id="ping_log", highlight=True)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_ping":
            host = self.query_one("#ping_host", Input).value
            count_str = self.query_one("#ping_count", Input).value
            count = int(count_str) if count_str.isdigit() else 4

            log = self.query_one("#ping_log", Log)
            log.clear()

            runner = PingRunner(host, count)

            def log_output(text: str):
                self.app.call_from_thread(log.write_line, text)

            self.run_worker(runner.run(log_output), exclusive=True)

class SocketTab(Container):
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Input(placeholder="Host", id="socket_host", value="1.1.1.1"),
            Input(placeholder="Port", id="socket_port", value="53", type="integer"),
            Select(
                (("TCP", "TCP"), ("UDP", "UDP")),
                prompt="Protocol",
                value="TCP",
                id="socket_protocol"
            ),
            Button("Test Connection", id="btn_socket_test", variant="primary"),
            id="socket_controls"
        )
        yield Log(id="socket_log", highlight=True)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_socket_test":
            host = self.query_one("#socket_host", Input).value
            port_str = self.query_one("#socket_port", Input).value
            protocol = self.query_one("#socket_protocol", Select).value

            if not host or not port_str or not protocol:
                return

            port = int(port_str)
            log = self.query_one("#socket_log", Log)
            log.clear()

            client = SocketClient(host, port, protocol)

            def log_output(text: str):
                self.app.call_from_thread(log.write_line, text)

            self.run_worker(client.test_connection(log_output), exclusive=True)

class SerialTab(Container):
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Input(placeholder="Port (e.g. /dev/ttyUSB0)", id="serial_port", value="/dev/ttyUSB0"),
            Input(placeholder="Baudrate", id="serial_baud", value="9600", type="integer"),
            Button("Connect", id="btn_serial_connect", variant="success"),
            Button("Disconnect", id="btn_serial_disconnect", variant="error", disabled=True),
            id="serial_controls"
        )
        yield Log(id="serial_log", highlight=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reader = None

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_serial_connect":
            port = self.query_one("#serial_port", Input).value
            baud_str = self.query_one("#serial_baud", Input).value
            baud = int(baud_str) if baud_str.isdigit() else 9600

            log = self.query_one("#serial_log", Log)

            self.reader = SerialReader(port, baud)

            def log_output(text: str):
                self.app.call_from_thread(log.write_line, text)

            self.query_one("#btn_serial_connect", Button).disabled = True
            self.query_one("#btn_serial_disconnect", Button).disabled = False

            self.run_worker(self.reader.connect(log_output), name="serial_worker")

        elif event.button.id == "btn_serial_disconnect":
            if self.reader:
                self.reader.stop()
                self.app.call_from_thread(self.query_one("#serial_log", Log).write_line, "Disconnected.")
            self.query_one("#btn_serial_connect", Button).disabled = False
            self.query_one("#btn_serial_disconnect", Button).disabled = True

class SnifferTab(Container):
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Input(placeholder="Interface (e.g. eth0, wlan0) - leave empty for default", id="sniffer_iface"),
            Input(placeholder="Count (0 for infinite)", id="sniffer_count", value="0", type="integer"),
            Button("Start Sniffing", id="btn_sniffer_start", variant="success"),
            Button("Stop Sniffing", id="btn_sniffer_stop", variant="error", disabled=True),
            id="sniffer_controls"
        )
        yield Log(id="sniffer_log", highlight=True, max_lines=1000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sniffer = None

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_sniffer_start":
            iface = self.query_one("#sniffer_iface", Input).value
            count_str = self.query_one("#sniffer_count", Input).value
            count = int(count_str) if count_str.isdigit() else 0

            if not iface:
                iface = None

            log = self.query_one("#sniffer_log", Log)

            self.sniffer = PacketSniffer(iface, count)

            def log_output(text: str):
                self.app.call_from_thread(log.write_line, text)

            self.sniffer.start(log_output)

            self.query_one("#btn_sniffer_start", Button).disabled = True
            self.query_one("#btn_sniffer_stop", Button).disabled = False

        elif event.button.id == "btn_sniffer_stop":
            if self.sniffer:
                self.sniffer.stop()
            self.query_one("#btn_sniffer_start", Button).disabled = False
            self.query_one("#btn_sniffer_stop", Button).disabled = True
