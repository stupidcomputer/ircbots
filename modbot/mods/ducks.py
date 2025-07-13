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

import utils
from irctokens import build, Line
import time
import random

def init(srv):
    srv.states['ducks'] = {
        'messages': 0,
        'duck': False,
        'last': time.time(),
    }

def privmsg(line, srv):
    if srv.states['ducks'] == None:
        init(srv)
    if not line.hostmask.nickname == "BitBotNewTest": srv.states['ducks']['messages'] += 1
    if random.randint(0, 99) <= 76 and srv.states['ducks']['messages'] > 1 and not srv.states['ducks']['duck']:
        srv.states['ducks']['duck'] = True
        srv.send(build('PRIVMSG', [line.params[0], 'a duck has appeared!']))
        srv.states['ducks']['messages'] = 0

def cmd(line, srv):
    command, params = utils.cmdparse(line)
    if command == "bef":
        if srv.states['ducks']['duck']:
            utils.message(srv, line.params[0], "you cought a duck!")
            srv.states['ducks']['duck'] = False
        else:
            utils.message(srv, line.params[0], "oh noes, you didn't catch it!")
