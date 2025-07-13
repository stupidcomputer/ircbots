import asyncio

from irctokens import build, Line
from ircrobots import Bot as BaseBot
from ircrobots import Server as BaseServer
from ircrobots import ConnectionParams

CHANNEL = "#testchannel"

class Server(BaseServer):
    coins = 0
    async def line_read(self, line: Line):
        print(f"{self.name} < {line.format()}")
        if line.command == "001":
            print(f"connected to {self.isupport.network}")
            await self.send(build("JOIN", [CHANNEL]))
            await self.send(build("PRIVMSG", ["NickServ", "identify randomuser_bots"]))
            await self.send(build("PRIVMSG", [CHANNEL, ",redeemcoins"]))
            asyncio.create_task(self.coin_harvest())
        elif line.command == "PRIVMSG" and line.hostmask.nickname == "tildebot" and self.params.nickname in line.params[1]:
            if "and wins" in line.params[1]:
                self.coins += float(line.params[1].split(' ')[6])
                if self.coins > 100:
                    print(self.coins)
                    await self.send(build("PRIVMSG", [CHANNEL, ",sendcoins rndusr {}".format(str(self.coins - 100))]))
                    self.coins = 100
                await self.flip()
            elif "and loses" in line.params[1]:
                self.coins -= float(line.params[1].split(' ')[6])
                if self.coins == 0:
                    asyncio.create_task(self.coin_sleep())
            elif "Please wait" in line.params[1]:
                await asyncio.sleep(1 * 60)
                await self.coin_harvest()
            elif "You can only reddem" in line.params[1]:
                asyncio.create_task(self.coin_sleep())

    def tildebot_here(self):
        try: return 'tildebot' in self.channels[CHANNEL].users
        except: return False
    async def line_send(self, line: Line):
        print(f"{self.name} > {line.format()}")
    async def flip(self):
        await self.send(build("PRIVMSG", [CHANNEL, ",flip heads all"]))
    async def bot_init(self):
        await asyncio.sleep(10)
        await self.flip()
        await self.send(build("PRIVMSG", [CHANNEL, "task started"]))
    async def coin_sleep(self):
        await asyncio.sleep(10 * 60 + 20)
        await self.send(build("PRIVMSG", ["#testchannel", ",redeemcoins"]))
        self.coins = 100
        await self.flip()
    async def coin_harvest(self):
        await self.send(build("PRIVMSG", ["#testchannel", ",redeemcoins"]))
        self.coins = 100
        await self.flip()

class Bot(BaseBot):
    def create_server(self, name: str):
        return Server(self, name)

async def main():
    bot = Bot()
    for i in [1]:
        params = ConnectionParams("rndus" + str(i), "localhost", 6667, False)
        await bot.add_server("tilde" + str(i), params)

    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())
