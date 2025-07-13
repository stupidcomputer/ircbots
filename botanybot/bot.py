import asyncio
import os
import random
import time
import subprocess

from irctokens import build, Line
from ircrobots import Bot as BaseBot
from ircrobots import Server as BaseServer
from ircrobots import ConnectionParams

from botany import IRCBotany as Botany
from admin import Admin

from secrets import PASSWORD

channels = [
    "#bots",
    "#club",
    "###",
    "#forero",
]
helpmessage = "hey, i'm botanybot. i water plants on ~club. my prefix is % and i was made by randomuser. check out https://ttm.sh/Fs4.txt for more information."

def userchooser(user):
    return random.choice([i for i in os.listdir(r"/home") if i.lower()[0] == user.lower()[0]])

# borrowed from kiedtl/ircbot
async def _aexec(self, code):
    # Make an async function with the code and `exec` it
    exec(f"async def __ex(self): " + "".join(f"\n {l}" for l in code.split("\n")))

    # Get `__ex` from local variables, call it and return the result
    return await locals()["__ex"](self)

class Server(BaseServer):
    admin = Admin('rndusr')
    async def msg(self, chan, string, user=None):
        if user == None: await self.send(build("PRIVMSG", [chan, string]))
        else: await self.send(build("PRIVMSG", [chan, user + ": " + string]))
    def isDrunk(self):
        if abs(self.drunkentime - int(time.time())) > 60 * 4: return True
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
            if line.params[-1] == "!rollcall":
                await self.msg(user, helpmessage, user)
            if line.params[-1] == "!botlist":
                await self.msg(user, helpmessage, user)
            if line.params[-1][0] == '%':
                commands = line.params[-1][1:].split(' ')
                if commands[0] == "score":
                    if len(commands) == 1: commands.append(user)
                    if self.isDrunk(): b = Botany(commands[1])
                    else:
                        b = Botany(userchooser(commands[1]))
                        while b.getInfo() == []:
                            b = Botany(userchooser(commands[1]))
                    i = b.getInfo()
                    await self.msg(user, "{}'s score: {}".format(b.user, str(int(b.score()))), user)
                elif commands[0] == "online":
                    proc = subprocess.Popen('w', stdout=subprocess.PIPE)
                    try: out, err = proc.communicate(timeout=10)
                    except:
                        proc.kill()
                        return
                    out = out.decode("utf-8")
                    out = out.split("\n")
                    out = len(set([i.split(" ")[0] for i in out][2:-1]))
                    await self.msg(user, "{} users are currently online".format(out), user)

                elif commands[0] == "pct":
                    if len(commands) == 1: commands.append(user)
                    b = Botany(commands[1])
                    i = b.getInfo()
                    await self.msg(user, "warning: the %pct command is experimental and could possibly not work. you have been warned.", user)
                    if len(i) > 1:
                        pct = max((1 - ((time.time() - i['last_watered'])/86400)) * 100, 0)
                        await self.msg(user, "plant percentage for {}: {}%".format(b.user, int(pct)), user)
                    else:
                        await self.msg(user, "couldn't find plant for {}".format(commands[1]), user)
                elif commands[0] == "vodka":
                    if self.isDrunk():
                        self.drunkentime = int(time.time())
                        await self.msg(user, "glug glug glug", user)
                    else:
                        await self.msg(user, "vodka? what's vodka? *burp*", user)
                elif commands[0] == "desc":
                    if len(commands) == 1: commands.append(user)
                    if self.isDrunk():
                        b = Botany(commands[1])
                    else:
                        b = Botany(userchooser(commands[1]))
                    await self.msg(user, b.plantDescription(), user)
                elif commands[0] == "water":
                    if len(commands) == 1: commands.append(user)
                    if self.isDrunk():
                        b = Botany(commands[1])
                        if b.water("{} (via IRC)".format(user)):
                            await self.msg(user, b.watered(), user)
                        else:
                            await self.msg(user, b.cantWater(), user)
                    else:
                        b = Botany(userchooser(commands[1]))
                        while not b.water("{} (via IRC)".format(user)):
                            b = Botany(userchooser(commands[1]))
                        await self.msg(user, b.watered(), user)
                elif commands[0] == "help":
                    await self.msg(user, helpmessage, user)
                elif commands[0] == "join":
                    if len(commands) == 2:
                        if user == self.admin:
                            await self.send(build("JOIN", [commands[1]]))
                            await self.msg(user, "joined the user {}".format(commands[1]), user)
                        else:
                            await self.msg(user, "you're not an admin", user)
                    else:
                        await self.msg(user, "specify the user", user)
                elif commands[0] == "addowner":
                    if len(commands) == 2:
                        if user == self.admin:
                            self.admin.append(commands[1])
                            await self.msg(user, "admin added: {}".format(commands[1]), user)
                            return
                        else:
                            await self.msg(user, "error: you must be an admin!", user)
                            return
                    else:
                        await self.msg(user, "two arguments required", user)
                        return
                elif commands[0] == "delowner":
                    if len(commands) == 2:
                        if user == self.admin:
                            try: self.admin.remove(commands[1])
                            except:
                                await self.msg(user, "problem with removing admin", user)
                                return
                            await self.msg(user, "admin deleted: {}".format(commands[1]), user)
                            return
                        else:
                            await self.msg(user, "error: you must be an admin!", user)
                            return
                    else:
                        await self.msg(user, "two arguments required", user)
                        return
                elif commands[0] == "amowner":
                    if user == self.admin:
                        await self.msg(user, "you're an admin", user)
                    else:
                        await self.msg(user, "you're not an admin", user)
                elif commands[0] == "ping": await self.msg(user, "pong", user)
                elif commands[0] == "eval":
                    if user == self.admin:
                        text = ' '.join(line.params[-1][1:].split(' ')[1:])
                        try:
                            result = await _aexec(self, text)
                        except Exception as e:
                            await self.msg(user, "segfault: {}".format(repr(e)), user)
                            return
                        await self.msg(user, "{}".format(result), user)
                    else:
                        await self.msg(user, "must have admin to execute", user)


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
