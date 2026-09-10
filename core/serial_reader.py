import asyncio
import serial_asyncio

class SerialReader:
    def __init__(self, port: str, baudrate: int = 9600):
        self.port = port
        self.baudrate = baudrate
        self.reader = None
        self.writer = None
        self._running = False

    async def connect(self, output_callback):
        try:
            self.reader, self.writer = await serial_asyncio.open_serial_connection(url=self.port, baudrate=self.baudrate)
            self._running = True
            if output_callback:
                output_callback(f"Connected to {self.port} at {self.baudrate} baud.")

            while self._running:
                line = await self.reader.readline()
                if line and output_callback:
                    output_callback(line.decode('utf-8', errors='replace').rstrip())
        except Exception as e:
            if output_callback:
                output_callback(f"Serial connection error: {e}")
            self.stop()

    def stop(self):
        self._running = False
        if self.writer:
            self.writer.close()
            self.writer = None
        self.reader = None
