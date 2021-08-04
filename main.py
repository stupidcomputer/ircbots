import asyncio

from irctokens import build, Line
from ircrobots import Bot as BaseBot
from ircrobots import Server as BaseServer
from ircrobots import ConnectionParams

SERVERS = [
    ("tilde", "localhost")
]

class Server(BaseServer):
    async def line_read(self, line: Line):
        print(f"{self.name} < {line.format()}")
        if line.command == "001":
            print(f"connected to {self.isupport.network}")
            await self.send(build("JOIN", ["#testchannel"]))
            task = asyncio.create_task(self.async_hello())
            await self.send(build("PRIVMSG", ["#testchannel", "task started"]))
    async def line_send(self, line: Line):
        print(f"{self.name} > {line.format()}")
    async def async_hello(self):
        await asyncio.sleep(10)
        self.send(build("PRIVMSG", ["#testchannel", "hello"]))

class Bot(BaseBot):
    def create_server(self, name: str):
        return Server(self, name)

async def main():
    bot = Bot()
    for name, host in SERVERS:
        params = ConnectionParams("BitBotNewTest", host, 6667, False)
        await bot.add_server(name, params)

    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())
