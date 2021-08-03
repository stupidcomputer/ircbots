from irctokens import build

def message(srv, channel, msg):
    srv.send(build("PRIVMSG", [channel, msg]))
