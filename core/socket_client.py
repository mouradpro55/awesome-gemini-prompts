import asyncio
import time

class SocketClient:
    def __init__(self, host: str, port: int, protocol: str = 'TCP'):
        self.host = host
        self.port = port
        self.protocol = protocol.upper()

    async def test_connection(self, output_callback):
        start_time = time.time()
        try:
            if self.protocol == 'TCP':
                if output_callback:
                    output_callback(f"Connecting to {self.host}:{self.port} via TCP...")

                # Try to open connection with a timeout
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(self.host, self.port),
                    timeout=5.0
                )

                elapsed = (time.time() - start_time) * 1000
                if output_callback:
                    output_callback(f"TCP Connection established in {elapsed:.2f} ms.")

                writer.close()
                await writer.wait_closed()
                if output_callback:
                    output_callback("Connection closed.")

            elif self.protocol == 'UDP':
                if output_callback:
                    output_callback(f"Sending UDP packet to {self.host}:{self.port}...")

                # For UDP, we create a datagram endpoint. UDP is connectionless.
                class UDPProtocol(asyncio.DatagramProtocol):
                    def __init__(self, cb):
                        self.cb = cb
                        self.transport = None

                    def connection_made(self, transport):
                        self.transport = transport
                        elapsed = (time.time() - start_time) * 1000
                        if self.cb:
                            self.cb(f"UDP Socket created in {elapsed:.2f} ms.")
                        transport.sendto(b"ping")
                        if self.cb:
                            self.cb("Sent 'ping' via UDP.")

                    def datagram_received(self, data, addr):
                        if self.cb:
                            self.cb(f"Received {data.decode(errors='ignore')} from {addr}")

                    def error_received(self, exc):
                        if self.cb:
                            self.cb(f"UDP error: {exc}")

                    def connection_lost(self, exc):
                        pass

                loop = asyncio.get_running_loop()
                transport, protocol = await asyncio.wait_for(
                     loop.create_datagram_endpoint(
                         lambda: UDPProtocol(output_callback),
                         remote_addr=(self.host, self.port)
                     ),
                     timeout=5.0
                )

                # Leave it open briefly to catch replies
                await asyncio.sleep(2)
                transport.close()

            else:
                 if output_callback:
                    output_callback(f"Unsupported protocol: {self.protocol}")

        except asyncio.TimeoutError:
            if output_callback:
                output_callback(f"Connection timeout after 5.0 seconds.")
        except ConnectionRefusedError:
            if output_callback:
                output_callback(f"Connection refused by {self.host}:{self.port}")
        except Exception as e:
            if output_callback:
                output_callback(f"Error testing connection: {e}")
