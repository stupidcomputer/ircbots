#!/usr/bin/env python3
import asyncio
from importlib import import_module as mod_include

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
PREFIX = '*'

class Server(BaseServer):
    handlers = {i: [] for i in EVENTS}
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
                self.handlers[i].append(getattr(mod, i))
        self.states[name] = None

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
                i(line, self)
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
    asyncio.run(main())
