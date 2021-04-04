#!/bin/python

import asyncio
import time
import sys

from irctokens import build, Line
from ircrobots import Bot as BaseBot
from ircrobots import Server as BaseServer
from ircrobots import ConnectionParams
from ircrobots.glob import compile as gcompile

SERVERS = [
    ("tilde", "localhost")
]
SPAMSERVERS = [
    ("0", "localhost"),
    ("1", "localhost"),
    ("2", "localhost"),
    ("3", "localhost"),
    ("4", "localhost"),
    ("5", "localhost"),
    ("6", "localhost"),
    ("7", "localhost"),
    ("8", "localhost"),
    ("9", "localhost"),
    ("10", "localhost"),
    ("11", "localhost"),
    ("12", "localhost"),
    ("13", "localhost"),
    ("14", "localhost"),
    ("15", "localhost"),
    ("16", "localhost"),
    ("17", "localhost"),
    ("18", "localhost"),
    ("19", "localhost"),
]
KICKEES = []
KICKEES_HOSTMASK = []
EXEMPT = []
MESSAGES = {
    "revenge": "no u",
    "kick": "error 418",
    "quit": "bonk",
    "kickadd": "user added to kicklist",
    "kickadderr": "adding failed: user on exemption list",
    "kicklist": "kickees: ",
    "kickrm": "user removed from kicklist",
    "kickrmerr": "error removing user from kicklist",
    "exemptadd": "user added to exemptlist",
    "exemptlist": "exempt: ",
    "exemptrm": "user removed from exemptlist",
    "exemptrmerr": "error removing user from exemptlist",
    "writeexempt": "writing exempt data",
    "writekickee": "writing kickee data",
    "writekickeehostmask": "writing kickee_hostmask data",
    "writedone": "done!",
    "writeerr": "error writing files"
}
CHANNEL = "#chaos"
PASSWORD = "hellothereperson"
BOTNAME = "rndbot"
OWNER = "rndusr"
TOPIC = "rule one: you are now a duck. ・゜゜・。。・゜゜\\_o< QUACK!"
SPAMUSER = ""

LOGFILE = open(CHANNEL + ".log", "w")

class SpamServer(BaseServer):
    async def line_read(self, line: Line):
        print(f"{self.name} < {line.format()}")
        if line.command == "001":
            asyncio.create_task(self.send(build("JOIN", [CHANNEL])))
        if line.command == "PRIVMSG" and line.params[0] == CHANNEL:
            if "quit" in line.params[1] and line.hostmask.nickname == OWNER:
                asyncio.create_task(self.send(build("PRIVMSG", [CHANNEL, "merp"])))
                asyncio.create_task(self.send(build("PART", [CHANNEL, "merp"])))
                asyncio.create_task(self.send(build("QUIT")))
            else:
                asyncio.create_task(self.send(build("PRIVMSG", [CHANNEL, "ALL HAIL IRES"])))
        if line.command == "KICK":
            if line.params[1] == BOTNAME:
                time.sleep(1)
                asyncio.create_task(self.send(build("JOIN", [CHANNEL])))
#                asyncio.create_task(build('KICK', [CHANNEL, line.params[2], MESSAGES['revenge']]))
    async def line_send(self, line: Line):
        print(f"{self.name} > {line.format()}")

class Server(BaseServer):
    async def line_read(self, line: Line):
        print(f"{self.name} < {line.format()}")
        LOGFILE.write(f"{self.name} < {line.format()}")
        if line.command == "001":
            await self.send(build("PRIVMSG", ["NickServ", "identify " + PASSWORD]))
            await self.send(build("MODE", [BOTNAME, "+B"]))
            await self.send(build("JOIN", [CHANNEL]))
        if line.command == "474":
            await self.send(build("PRIVMSG", ["ChanServ", "unban " + CHANNEL + " " + BOTNAME]))
            await self.send(build("PRIVMSG", ["ChanServ", "owner " + CHANNEL + " " + BOTNAME]))
            await self.send(build("PRIVMSG", ["ChanServ", "invite " + CHANNEL + " " + BOTNAME]))
            await self.send(build("JOIN", [CHANNEL]))
        if line.command == "PRIVMSG" and line.params[0] == CHANNEL:
            if line.hostmask.nickname == OWNER:
                if BOTNAME + ": quit" == line.params[1]:
                    await self.send(build('PART', [CHANNEL, MESSAGES['quit']]))
                    exit(100)
                if BOTNAME + ": kickadd" in line.params[1]:
                    if gcompile("*!*@*").match(line.params[1].split(' ')[2]):
                            KICKEES_HOSTMASK.append(line.params[1].split(' ')[2])
                            await self.send(build('PRIVMSG', [CHANNEL, \
                                MESSAGES['kickadd']]))
                    else:
                        if not line.params[1].split(' ')[1] in EXEMPT:
                            KICKEES.append(line.params[1].split(' ')[2])
                            await self.send(build('PRIVMSG', [CHANNEL, \
                                MESSAGES['kickadd']]))
                        else:
                            await self.send(build('PRIVMSG', [CHANNEL, \
                                MESSAGES['kickadderr']]))
                if BOTNAME + ": kicklist" in line.params[1]:
                    await self.send(build('PRIVMSG', [CHANNEL, \
                            MESSAGES['kicklist'] + ' '.join(KICKEES)]))
                    await self.send(build('PRIVMSG', [CHANNEL, \
                            MESSAGES['kicklist'] + ' '.join(KICKEES_HOSTMASK)]))
                if BOTNAME + ": kickrm" in line.params[1]:
                    try:
                        if gcompile("*!*@*").match(line.params[1].split(' ')[2]):
                            KICKEES_HOSTMASK.remove(line.params[1].split(' ')[2])
                        else:
                            KICKEES.remove(line.params[1].split(' ')[2])
                        await self.send(build('PRIVMSG', [CHANNEL, \
                            MESSAGES['kickrm']]))
                    except ValueError:
                        await self.send(build('PRIVMSG', [CHANNEL, \
                            MESSAGES['kickrmerr']]))
                if BOTNAME + ": exemptadd" in line.params[1]:
                    EXEMPT.append(line.params[1].split(' ')[2])
                    await self.send(build('PRIVMSG', [CHANNEL, \
                        MESSAGES['exemptadd']]))
                if BOTNAME + ": exemptlist" in line.params[1]:
                    await self.send(build('PRIVMSG', [CHANNEL, \
                            MESSAGES['exemptlist'] + ' '.join(EXEMPT)]))
                if BOTNAME + ": exemptrm" in line.params[1]:
                    try:
                        EXEMPT.remove(line.params[1].split(' ')[2])
                        await self.send(build('PRIVMSG', [CHANNEL, \
                            MESSAGES['exemptrm']]))
                    except ValueError:
                        await self.send(build('PRIVMSG', [CHANNEL, \
                            MESSAGES['exemptrmerr']]))
                if BOTNAME + ": ping" in line.params[1]:
                    tmp = ""
                    for i in self.channels[CHANNEL].users.keys():
                        tmp += i
                        tmp += ' '
                        if len(tmp) > 100:
                            await self.send(build('PRIVMSG', [CHANNEL, \
                                tmp]))
                            tmp = ""
                    await self.send(build('PRIVMSG', [CHANNEL, \
                        tmp]))
                if BOTNAME + ": savestate" in line.params[1]:
                    try:
                        fd = open("kickees", "w")
                        await self.send(build('PRIVMSG', [CHANNEL, MESSAGES['writekickee']]))
                        fd.writelines(i + '\n' for i in KICKEES)
                        fd.close()
                        fd = open("kickees_mask", "w")
                        await self.send(build('PRIVMSG', [CHANNEL, MESSAGES['writekickeehostmask']]))
                        fd.writelines(i + '\n' for i in KICKEES_HOSTMASK)
                        fd.close()
                        await self.send(build('PRIVMSG', [CHANNEL, MESSAGES['writeexempt']]))
                        fd = open("exempt", "w")
                        fd.writelines(i + '\n' for i in EXEMPT)
                        fd.close()
                        await self.send(build('PRIVMSG', [CHANNEL, MESSAGES['writedone']]))
                    except:
                        await self.send(build('PRIVMSG', [CHANNEL, MESSAGES['writeerr']]))
                if BOTNAME + ": bots" in line.params[1]:
                    bot = SpamBot()
                    for name, host in SPAMSERVERS:
                        await bot.add_server(name, \
                            ConnectionParams(BOTNAME + name, host, 6667, False, BOTNAME))
                        asyncio.create_task(bot.run())
                if BOTNAME + ": kick" in line.params[1]:
                    for i in self.channels[CHANNEL].users:
                        if i != OWNER:
                            asyncio.create_task(self.send(build('KICK', [CHANNEL, i, 'nope'])))

        if line.command == "JOIN":
            if line.hostmask.nickname in KICKEES:
                await self.send(build('KICK', [CHANNEL, line.hostmask.nickname, MESSAGES['kick']]))
            else:
                for i in KICKEES_HOSTMASK:
                    if gcompile(i).match(str(line.hostmask)):
                        await self.send(build('KICK', [CHANNEL, line.hostmask.nickname, MESSAGES['kick']]))
                        break
        if line.hostmask.nickname == "bot":
            global TASKCACHE
            TASKCACHE = asyncio.create_task(self.julian())
        if line.command == "PART":
            if line.hostmask.nickname == 'bot' and 'TASKCACHE' in globals():
                TASKCACHE.cancel()
        if line.command == "QUIT":
            if line.hostmask.nickname == 'bot' and 'TASKCACHE' in globals():
                TASKCACHE.cancel()
        if line.command == "MODE":
            try:
                if 'l' in self.channels[CHANNEL].modes:
                    await self.send(build('MODE', [CHANNEL, '-l']))
                if 'n' in self.channels[CHANNEL].modes:
                    await self.send(build('MODE', [CHANNEL, '-n']))
                if 'm' in self.channels[CHANNEL].modes:
                    await self.send(build('MODE', [CHANNEL, '-m']))
                if 's' in self.channels[CHANNEL].modes:
                    await self.send(build('MODE', [CHANNEL, '-s']))
                if not 'q' in self.channels[CHANNEL].users[OWNER].modes:
                    await self.send(build('MODE', [CHANNEL, '+q', OWNER]))
                if 'b' in self.channels[CHANNEL].users[BOTNAME].modes:
                    await self.send(build("PRIVMSG", ["ChanServ", "unban " + CHANNEL + " " + BOTNAME]))
                if not 'q' in self.channels[CHANNEL].users[BOTNAME].modes:
                    await self.send(build("PRIVMSG", ["ChanServ", "owner " + CHANNEL + " " + BOTNAME]))
                else:
                    print(self.channels[CHANNEL].modes)
            except KeyError:
                pass
        if line.command == "KICK" and line.params[0] == CHANNEL:
            if line.params[1] == OWNER:
                await self.send(build('KICK', [CHANNEL, line.hostmask.nickname, MESSAGES['revenge']]))
                await self.send(build('INVITE', [CHANNEL, line.params[1]]))
            if line.params[1] == BOTNAME:
                time.sleep(1)
                await self.send(build('JOIN', [CHANNEL]))
                time.sleep(0.5)
                await self.send(build('KICK', [CHANNEL, line.hostmask.nickname, MESSAGES['revenge']]))
        if line.command == "TOPIC" and line.params[0] == CHANNEL:
            if line.hostmask.nickname != OWNER and \
                line.hostmask.nickname != BOTNAME and \
                not line.hostmask.nickname in EXEMPT:
                await self.send(build('TOPIC', [CHANNEL, TOPIC]))
        if line.command == "482":
            await self.send(build('TOPIC', [CHANNEL, TOPIC]))

    async def line_send(self, line: Line):
        print(f"{self.name} > {line.format()}")
        LOGFILE.write(f"{self.name} > {line.format()}")

    async def julian(self):
        while True:
            self.send(build('PRIVMSG', [CHANNEL, "hi"]))

class Bot(BaseBot):
    def create_server(self, name: str):
        return Server(self, name)

class SpamBot(BaseBot):
    def create_server(self, name: str):
        return SpamServer(self, name)

async def main():
    try:
        fd = open("kickees", "r")
        for i in fd.readlines():
            if not i in EXEMPT:
                KICKEES.append(i.rstrip('\n'))
        fd.close()
        fd = open("kickees_mask", "r")
        for i in fd.readlines():
            if not i in EXEMPT:
                KICKEES_HOSTMASK.append(i.rstrip('\n'))
        fd.close()
        fd = open("exempt", "r")
        for i in fd.readlines():
            EXEMPT.append(i.rstrip('\n'))
        fd.close()
    except FileNotFoundError:
        print("warning: save state files are missing")
        print("proceeding without save state files")
    bot = Bot()
    for name, host in SERVERS:
        params = ConnectionParams(BOTNAME, host, 6667, False, BOTNAME, "totally not rndusr's bot lol")
        await bot.add_server(name, params)

    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())
