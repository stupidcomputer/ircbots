import utils

def cmd(line, srv):
    command, params = utils.cmdparse(line)
    if command == "load":
        try:
            srv.load_mod(params[0])
        except ModuleNotFoundError:
            utils.message(srv, line.params[0],
                "failed to load `" + params[0] + "'")
        else:
            utils.message(srv, line.params[0],
                "loaded: `" + params[0] + "'")
    elif command == "unload":
        try:
            srv.unload_mod(params[0])
        except:
            utils.message(srv, line.params[0],
                "failed to unload `" + params[0] + "'")
        else:
            utils.message(srv, line.params[0],
                "unloaded: `" + params[0] + "'"
