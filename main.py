#!/usr/bin/env python3
# modbot is copyright rndusr/randomuser 2021
# This file is part of modbot.

# modbot is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any
# later version.

# modbot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero
# General Public License along with modbot.  If not, see
# <https://www.gnu.org/licenses/>.

import asyncio
from importlib import import_module as mod_include
import os
import sys

from irctokens import build, Line
from ircrobots import Bot as BaseBot
from ircrobots import Server as BaseServer
from ircrobots import ConnectionParams

SERVERS = [
    ("beep", "beepboop.systems")
]
EVENTS = [
    "cmd",
    "privmsg",
    "topic",
    "mode",
    "kick",
    "join",
    "part",
    "invite",
]
ADMINS = ['rndusr']
PREFIX = '*'

class Admin:
    def __init__(self, nick):
        self.nicks = []
        self.nicks.append(nick)
    def __eq__(self, val):
        return val in self.nicks
    def append(self, nick):
        self.nicks.append(nick)
    def remove(self, nick):
        self.nicks.remove(nick)

class Server(BaseServer):
    handlers = {i: [] for i in EVENTS}
    admins = [Admin(i) for i in ADMINS]
    states = {}
    async def line_read(self, line: Line):
        print(f"{self.name} < {line.format()}")
        if line.command == "001":
            await self.send(build("JOIN", ["#testchannel"]))
            self.load_mod("default")
        self.event_handle(line)

    def load_mod(self, name):
        mod = mod_include(name)
        for i in EVENTS:
            if hasattr(mod, i):
                self.handlers[i].append([name, getattr(mod, i)])
        self.states[name] = None

    def unload_mod(self, name):
        for i in EVENTS:
            self.handlers[i] = [j for j in self.handlers[i] if not j[0] == name]

    def event_get(self, line: Line):
        if line.command.lower() in EVENTS[2:]:
            return line.command.lower()
        elif line.command.lower() == "privmsg":
            if line.params[1][0] == PREFIX: return "cmd"
            else: return "privmsg"
        else:
            # something has gone horribly, horribly wrong
            return None

    def event_handle(self, line: Line):
        event = self.event_get(line)
        if event == None: return False
        try:
            for i in self.handlers[event]:
                ret = i[1](line, self)
                if not ret == None:
                    self.states[i[0]] = ret
        except IndexError: return False
        return True

    async def line_send(self, line: Line):
        print(f"{self.name} > {line.format()}")

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
    os.chdir("mods")
    sys.path = [os.getcwd()] + sys.path
    asyncio.run(main())
