import asyncio

from irctokens import build, Line
from ircrobots import Bot as BaseBot
from ircrobots import Server as BaseServer
from ircrobots import ConnectionParams

from botany import IRCBotany as Botany

from secrets import PASSWORD

channels = [
    "#bots",
#    "#club",
]
helpmessage = "hey, i'm botanybot. i water plants on ~club. my prefix is % and i was made by randomuser. check out https://ttm.sh/Fki.txt for more information."

class Server(BaseServer):
    admin = 'rndusr'
    async def msg(self, chan, string, user=None):
        if user == None: await self.send(build("PRIVMSG", [chan, string]))
        else: await self.send(build("PRIVMSG", [chan, user + ": " + string]))
    async def line_read(self, line: Line):
        print(f"{self.name} < {line.format()}")
        if line.command == "001":
            await self.send(build("MODE", ["botanybot", "+B"]))
            await self.msg("nickserv", "identify " + PASSWORD)
            for i in channels:
                await self.send(build("JOIN", [i]))
        if line.command == "PRIVMSG":
            user = line.hostmask.nickname
            channel = line.params[0]
            if line.params[-1] == "!rollcall":
                await self.msg(channel, helpmessage, user)
            if line.params[-1][0] == '%':
                commands = line.params[-1][1:].split(' ')
                if commands[0] == "desc":
                    if len(commands) == 2:
                        b = Botany(commands[1])
                        await self.msg(channel, b.plantDescription(), user)
                    else:
                        await self.msg(channel, "specify user", user)
                elif commands[0] == "water":
                    if len(commands) == 2:
                        b = Botany(commands[1])
                        if(b.water("{} (via IRC)".format(user))):
                            await self.msg(channel, b.watered(), user)
                        else:
                            await self.msg(channel, b.cantWater(), user)
                elif commands[0] == "help":
                    await self.msg(channel, helpmessage, user)
                elif commands[0] == "join":
                    if len(commands) == 2:
                        if user == self.admin:
                            await self.send(build("JOIN", [commands[1]]))
                            await self.msg(channel, "joined the channel {}".format(commands[1]), user)
                elif commands[0] == "chowner":
                    if len(commands) == 2:
                        if user == self.admin:
                            self.admin = commands[1]
                            await self.msg(channel, "admin changed to {}".format(commands[1]), user)
                            return
                        else:
                            await self.msg(channel, "error: you must be an admin!", user)
                            return
                    else:
                        await self.msg(channel, "two arguments required", user)
                        return
    async def line_send(self, line: Line):
        print(f"{self.name} > {line.format()}")

class Bot(BaseBot):
    def create_server(self, name:str):
        return Server(self, name)

async def main():
    bot = Bot()
    params = ConnectionParams("botanybot", "tilde.chat", 6697, True)
    await bot.add_server("tilde", params)
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())
