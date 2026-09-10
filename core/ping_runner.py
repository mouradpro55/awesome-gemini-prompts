import asyncio
import platform

class PingRunner:
    def __init__(self, host: str, count: int = 4):
        self.host = host
        self.count = count
        self.process = None

    async def run(self, output_callback):
        # Determine the ping command arguments based on OS
        param = '-n' if platform.system().lower() == 'windows' else '-c'

        try:
            self.process = await asyncio.create_subprocess_exec(
                'ping', param, str(self.count), self.host,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            while True:
                line = await self.process.stdout.readline()
                if not line:
                    break
                # Call the callback with the decoded line
                if output_callback:
                    output_callback(line.decode('utf-8', errors='replace').rstrip())

            await self.process.wait()

        except Exception as e:
            if output_callback:
                output_callback(f"Error running ping: {e}")

    def stop(self):
        if self.process and self.process.returncode is None:
            try:
                self.process.terminate()
            except ProcessLookupError:
                pass
