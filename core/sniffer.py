import asyncio
from scapy.all import sniff, IP, TCP, UDP
import threading

class PacketSniffer:
    def __init__(self, interface: str = None, count: int = 0):
        self.interface = interface
        self.count = count
        self._running = False
        self._thread = None
        self.output_callback = None

    def _packet_handler(self, packet):
        if not self._running:
            return True # Stop sniffing

        summary = packet.summary()

        # Add a bit more detail if it's IP
        if IP in packet:
            src = packet[IP].src
            dst = packet[IP].dst
            proto = packet[IP].proto

            detail = f"{src} -> {dst} (Proto: {proto})"

            if TCP in packet:
                detail += f" [TCP {packet[TCP].sport} -> {packet[TCP].dport}]"
            elif UDP in packet:
                detail += f" [UDP {packet[UDP].sport} -> {packet[UDP].dport}]"

            summary = f"{detail} | {summary}"

        if self.output_callback:
            # Need to call this safely if it's updating UI,
            # but usually textual message queues handle thread safety
            self.output_callback(summary)

    def _start_sniffing(self):
        try:
            kwargs = {
                "prn": self._packet_handler,
                "store": False,
                "stop_filter": lambda p: not self._running
            }
            if self.interface:
                kwargs["iface"] = self.interface
            if self.count > 0:
                kwargs["count"] = self.count

            sniff(**kwargs)
        except Exception as e:
            if self.output_callback:
                self.output_callback(f"Sniffer error: {e}")
        finally:
            self._running = False

    def start(self, output_callback):
        if self._running:
            return

        self.output_callback = output_callback
        self._running = True

        if self.output_callback:
             self.output_callback(f"Starting sniffer on {self.interface or 'default interface'}...")

        self._thread = threading.Thread(target=self._start_sniffing, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self.output_callback:
            self.output_callback("Sniffer stopped.")
