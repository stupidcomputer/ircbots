#!/bin/python

import asyncio
import time

from irctokens import build, Line
from ircrobots import Bot as BaseBot
from ircrobots import Server as BaseServer
from ircrobots import ConnectionParams
from ircrobots.glob import compile as gcompile

from nicklist import Nicklist
from text import MESSAGES
# contains PASSWORD = "merp"
from secrets import PASSWORD

kickees = Nicklist()
exempt = Nicklist()
CHANNEL = "#chaos"
BOTNAME = "rndbotmerp"
OWNER = "rndusr"
TOPIC = "rule one: you are now a duck. ・゜゜・。。・゜゜\\_o< QUACK!"
SPAMUSER = ""

LOGFILE = open(CHANNEL + ".log", "w")

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
                    exit(1)
                if BOTNAME + ": add" in line.params[1]:
                    if "kickees" == line.params[1].split(' ')[2]:
                        if kickees.append(line.params[1].split(' ')[3]):
                            await self.send(build('PRIVMSG', [CHANNEL, \
                                    MESSAGES['kickadd']]))
                        else:
                            await self.send(build('PRIVMSG', [CHANNEL, \
                                    MESSAGES['kickadderr']]))
                    if "exempt" == line.params[1].split(' ')[2]:
                        if exempt.append(line.params[1].split(' ')[3]):
                            await self.send(build('PRIVMSG', [CHANNEL, \
                                    MESSAGES['exemptadd']]))
                        else:
                            await self.send(build('PRIVMSG', [CHANNEL, \
                                    MESSAGES['exemptadderr']]))
                if BOTNAME + ": list" in line.params[1]:
                    if "kickees" == line.params[1].split(' ')[2]:
                        await self.send(build('PRIVMSG', [CHANNEL, \
                                MESSAGES['kicklist'] + str(kickees)]))
                    if "exempt" == line.params[1].split(' ')[2]:
                        await self.send(build('PRIVMSG', [CHANNEL, \
                                MESSAGES['exemptlist'] + str(exempt)]))
                if BOTNAME + ": rm" in line.params[1]:
                    if "kickees" == line.params[1].split(' ')[2]:
                        if kickees.remove(line.params[1].split(' ')[3]):
                            await self.send(build('PRIVMSG', [CHANNEL, \
                                MESSAGES['kickrm']]))
                        else:
                            await self.send(build('PRIVMSG', [CHANNEL, \
                                MESSAGES['kickrmerr']]))
                    if "exempt" == line.params[1].split(' ')[2]:
                        if exempt.remove(line.params[1].split(' ')[3]):
                            await self.send(build('PRIVMSG', [CHANNEL, \
                                MESSAGES['exemptrm']]))
                        else:
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
                if BOTNAME + ": writestate" in line.params[1]:
                    if kickees.write('kickee'):
                        await self.send(build('PRIVMSG', [CHANNEL, MESSAGES['writekickee']]))
                    if exempt.write('exempt'):
                        await self.send(build('PRIVMSG', [CHANNEL, MESSAGES['writeexempt']]))
                if BOTNAME + ": readstate" in line.params[1]:
                    if kickees.read('kickee'):
                        pass
                    if exempt.read('exempt'):
                        pass
                if BOTNAME + ": kickall" in line.params[1]:
                    for i in self.channels[CHANNEL].users:
                        if i != OWNER:
                            asyncio.create_task(self.send(build('KICK', [CHANNEL, i, 'nope'])))

        if line.command == "JOIN":
            if line.hostmask.nickname in kickees:
                await self.send(build('KICK', [CHANNEL, line.hostmask.nickname, MESSAGES['kick']]))
                return
            for i in kickees.host():
                if gcompile(i).match(str(line.hostmask)):
                    await self.send(build('KICK', [CHANNEL, line.hostmask.nickname, MESSAGES['kick']]))
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

class Bot(BaseBot):
    def create_server(self, name: str):
        return Server(self, name)

async def main():
    bot = Bot()
    params = ConnectionParams(BOTNAME, 'localhost', 6667, False, BOTNAME, "totally not rndusr's bot lol")
    await bot.add_server('tilde', params)
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())
