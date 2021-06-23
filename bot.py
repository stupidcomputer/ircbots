import asyncio
import os
import random
import time

from irctokens import build, Line
from ircrobots import Bot as BaseBot
from ircrobots import Server as BaseServer
from ircrobots import ConnectionParams

from botany import IRCBotany as Botany
from admin import Admin

from secrets import PASSWORD

channels = [
    "#bots",
#    "#club",
    "###",
]
helpmessage = "hey, i'm botanybot. i water plants on ~club. my prefix is % and i was made by randomuser. check out https://ttm.sh/FoF.txt for more information."

def userchooser(user):
    return random.choice([i for i in os.listdir(r"/home") if i[0] == user[0]])

class Server(BaseServer):
    admin = Admin('rndusr')
    async def msg(self, chan, string, user=None):
        if user == None: await self.send(build("PRIVMSG", [chan, string]))
        else: await self.send(build("PRIVMSG", [chan, user + ": " + string]))
    def isDrunk(self):
        if abs(self.drunkentime - int(time.time())) > 30: return True
        return False
    async def line_read(self, line: Line):
        print(f"{self.name} < {line.format()}")
        if line.command == "001":
            await self.send(build("MODE", ["botanybot", "+B"]))
            await self.msg("nickserv", "identify " + PASSWORD)
            for i in channels:
                await self.send(build("JOIN", [i]))
            self.drunkentime = 0
        if line.command == "PRIVMSG":
            user = line.hostmask.nickname
            channel = line.params[0]
            if line.params[-1] == "!rollcall":
                await self.msg(channel, helpmessage, user)
            if line.params[-1][0] == '%':
                commands = line.params[-1][1:].split(' ')
                if commands[0] == "score":
                    if len(commands) == 2:
                        if self.isDrunk(): b = Botany(commands[1])
                        else:
                            b = Botany(userchooser(commands[1]))
                            while b.getInfo() == []:
                                b = Botany(userchooser(commands[1]))
                        i = b.getInfo()
                        await self.msg(channel, "{}'s score: {}".format(b.user, str(int(b.score()))), user)
                elif commands[0] == "vodka":
                    if self.isDrunk():
                        self.drunkentime = int(time.time())
                        await self.msg(channel, "glug glug glug", user)
                    else:
                        await self.msg(channel, "vodka? what's vodka? *burp*", user)
                elif commands[0] == "desc":
                    if len(commands) == 2:
                        if self.isDrunk():
                            b = Botany(commands[1])
                        else:
                            b = Botany(userchooser(commands[1]))
                        await self.msg(channel, b.plantDescription(), user)
                    else:
                        await self.msg(channel, "specify user", user)
                elif commands[0] == "water":
                    if len(commands) == 2:
                        if self.isDrunk():
                            b = Botany(commands[1])
                            if b.water("{} (via IRC)".format(user)):
                                await self.msg(channel, b.watered(), user)
                            else:
                                await self.msg(channel, b.cantWater(), user)
                        else:
                            b = Botany(userchooser(commands[1]))
                            while not b.water("{} (via IRC".format(user)):
                                b = Botany(userchooser(commands[1]))
                            await self.msg(channel, b.watered(), user)
                elif commands[0] == "help":
                    await self.msg(channel, helpmessage, user)
                elif commands[0] == "join":
                    if len(commands) == 2:
                        if user == self.admin:
                            await self.send(build("JOIN", [commands[1]]))
                            await self.msg(channel, "joined the channel {}".format(commands[1]), user)
                elif commands[0] == "addowner":
                    if len(commands) == 2:
                        if user == self.admin:
                            self.admin.append(commands[1])
                            await self.msg(channel, "admin added: {}".format(commands[1]), user)
                            return
                        else:
                            await self.msg(channel, "error: you must be an admin!", user)
                            return
                    else:
                        await self.msg(channel, "two arguments required", user)
                        return
                elif commands[0] == "delowner":
                    if len(commands) == 2:
                        if user == self.admin:
                            try: self.admin.remove(commands[1])
                            except:
                                await self.msg(channel, "problem with removing admin", user)
                                return
                            await self.msg(channel, "admin deleted: {}".format(commands[1]), user)
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
