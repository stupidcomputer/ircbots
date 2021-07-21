import asyncio
import random
import time

from irctokens import build, Line
from ircrobots import Bot as BaseBot
from ircrobots import Server as BaseServer
from ircrobots import ConnectionParams

lang = {
    "noduck": "there was no duck! you missed by {} seconds!",
    "noduckstart": "there was no duck!",
    "duckcought": "duck has been cought by {} in channel {} in {} seconds!",
    "duck": "・゜゜・。。・゜゜\_o< QUACK!",
}

class Server(BaseServer):
    messages = 0
    duckactive = False
    duckactivetime = 0
    lastduck = 0
    async def msg(self, chan, msg, usr=None):
        if usr != None:
            await self.send(build("PRIVMSG", [chan, usr + ": " + msg]))
        else: await self.send(build("PRIVMSG", [chan, msg]))
    async def msgall(self, msg):
        [await self.msg(channel, msg) for channel in self.channels]
    async def new_duck(self):
        self.messages = 0
        self.duckactive = True
        self.duckactivetime = time.time()
        await self.msgall(lang["duck"])
    async def misstime(self):
        return format(time.time() - self.lastduck, '.2f')
    async def coughttime(self):
        return format(self.lastduck - self.duckactivetime, '.2f')
    async def duck_action(self, user, chan):
        if self.duckactive:
            self.duckactive = False
            self.messages = 0
            self.lastduck = time.time()
            await self.msgall(lang["duckcought"].format(user, chan, self.coughttime())))
        elif self.lastduck != 0:
            await self.msg(chan, lang["noduck"].format(self.coughttime())), user)
        else:
            await self.msg(chan, lang["noduckstart"], user)
    async def line_read(self, line: Line):
        print(f"{self.name} < {line.format()}")
        if line.command == "001":
            await self.send(build("JOIN", ["#testchannel"]))
        elif line.command == "PRIVMSG":
            print(line.params)
            print(line.hostmask.nickname)
            if line.params[1][0] == '%':
                cmd = line.params[1][1:]
                chan = line.params[0]
                user = line.hostmask.nickname
                if cmd == "bef": await self.duck_action(user, chan)
                if cmd == "trigger": await self.new_duck()
                return

            self.messages += 1
            if self.messages > 1 and random.randint(0, 100) < 10: await self.new_duck()
        elif line.command == "INVITE":
            await self.send(build("JOIN", [line.params[1]]))
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
