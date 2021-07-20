import asyncio
import random

from irctokens import build, Line
from ircrobots import Bot as BaseBot
from ircrobots import Server as BaseServer
from ircrobots import ConnectionParams

class Server(BaseServer):
    messages = 0
    duckactive = False
    async def line_read(self, line: Line):
        print(f"{self.name} < {line.format()}")
        if line.command == "001":
            await self.send(build("JOIN", ["#testchannel"]))
        if line.command == "PRIVMSG":
            if line.params[1][0] == '%':
                cmd = line.params[1][1:]
                if cmd == "bef":
                    if self.duckactive:
                        self.duckactive = False
                        await self.send(build("PRIVMSG", ["#testchannel", "you got the duck! congrats!"]))
                    else:
                        await self.send(build("PRIVMSG", ["#testchannel", "there was no duck!"]))

            self.messages += 1
            if self.messages > 1 and random.randint(0, 100) < 10:
                await self.send(build("PRIVMSG", ["#testchannel", "here's a duck!"]))
                self.messages = 0
                self.duckactive = True
    async def line_send(self, line: Line):
        print(f"{self.name} > {line.format()}")

class Bot(BaseBot):
    def create_server(self, name: str):
        return Server(self, name)

async def main():
    bot = Bot()
    params = ConnectionParams("test", "beepboop.systems", 6667, False)
    await bot.add_server("beep", params)
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())
