# bond Python interface setup
import io
import json
import os
import sys

try:
    import cPickle as pickle
except ImportError:
    import pickle


# Redirect normal output
def __BOND_buffer_stdio(obj):
    if isinstance(obj, io.TextIOBase):
        ret = io.TextIOWrapper(io.BytesIO())
        ret.getvalue = lambda: ret.buffer.getvalue().decode(ret.encoding)
    else:
        import cStringIO
        ret = cStringIO.StringIO()
    return ret

__BOND_BUFFERS = {
    "STDOUT": __BOND_buffer_stdio(sys.stdout),
    "STDERR": __BOND_buffer_stdio(sys.stderr)
}

def __BOND_raw_stdio(obj):
    return obj.buffer if isinstance(obj, io.TextIOBase) else obj

__BOND_CHANNELS = {
    "STDIN": __BOND_raw_stdio(sys.stdin),
    "STDOUT": __BOND_raw_stdio(sys.stdout),
    "STDERR": __BOND_raw_stdio(sys.stderr)
}


# Define our own i/o methods
def __BOND_getline():
    return __BOND_CHANNELS['STDIN'].readline().rstrip()

def __BOND_sendline(line=b''):
    stdout = __BOND_CHANNELS['STDOUT']
    stdout.write(line + b'\n')
    stdout.flush()

def __BOND_sendstate(state, code=None):
    line = bytes(state.encode('ascii'))
    if code is not None:
        line = line + b' ' + code
    __BOND_sendline(line)


# Serialization protocols
class __BOND_PICKLE(object):
    @staticmethod
    def dumps(*args):
        return repr(pickle.dumps(args, 0)).encode('utf-8')

    @staticmethod
    def loads(buf):
        dec = eval(buf.decode('utf-8'))
        if not isinstance(dec, bytes): dec = dec.encode('utf-8')
        return pickle.loads(dec)[0]


class __BOND_JSON(object):
    @staticmethod
    def loads(buf):
        return json.loads(buf.decode('utf-8'))

    @staticmethod
    def dumps(*args):
        return json.dumps(*args, skipkeys=False).encode('utf-8')


# Serialization methods
class _BOND_SerializationException(TypeError):
    pass

__BOND_PROTO = None

def __BOND_dumps(*args):
    try:
        ret = __BOND_PROTO.dumps(*args)
    except:
        raise _BOND_SerializationException("cannot encode {data}".format(data=str(args)))
    return ret

def __BOND_loads(buf):
    return __BOND_PROTO.loads(buf)


# Recursive repl
__BOND_TRANS_EXCEPT = None

def __BOND_remote(name, args):
    __BOND_sendstate("CALL", __BOND_dumps([name, args]))
    return __BOND_repl()

def __BOND_export(name):
    globals()[name] = lambda *args: __BOND_remote(name, args)

def __BOND_repl():
    SENTINEL = 1
    while True:
        line = __BOND_getline()
        if len(line) == 0:
            break

        line = line.split(b' ', 1)
        cmd = line[0].decode('ascii')
        args = __BOND_loads(line[1]) if len(line) > 1 else []

        ret = None
        err = None
        if cmd == "EVAL" or cmd == "EVAL_BLOCK":
            try:
                mode = 'eval' if cmd == "EVAL" else 'exec'
                ret = eval(compile(args, '<string>', mode), globals())
            except Exception as e:
                err = e

        elif cmd == "EXPORT":
            __BOND_export(args)

        elif cmd == "CALL":
            try:
                func = eval(args[0], globals())
                ret = func(*args[1])
            except Exception as e:
                err = e

        elif cmd == "XCALL":
            try:
                func = eval(args[0], globals())
                xargs = []
                for el in args[1]:
                    xargs.append(el[1] if not el[0] else eval(el[1], globals()))
                ret = func(*xargs)
            except Exception as e:
                err = e

        elif cmd == "RETURN":
            return args

        elif cmd == "EXCEPT":
            raise args if isinstance(args, Exception) else Exception(args)

        elif cmd == "ERROR":
            raise _BOND_SerializationException(args)

        else:
            exit(1)

        # redirected channels
        for chan, buf in __BOND_BUFFERS.items():
            if buf.tell():
                code = __BOND_dumps([chan, buf.getvalue()])
                __BOND_sendstate("OUTPUT", code)
                buf.truncate(0)

        # error state
        state = "RETURN"
        if err is not None:
            if isinstance(err, _BOND_SerializationException):
                state = "ERROR"
                ret = str(err)
            else:
                state = "EXCEPT"
                ret = err if __BOND_TRANS_EXCEPT else str(err)
        try:
            code = __BOND_dumps(ret)
        except Exception as e:
            state = "ERROR"
            code = __BOND_dumps(str(e))
        __BOND_sendstate(state, code)

    # stream ended
    return 0


def __BOND_start(proto, trans_except):
    global __BOND_PROTO, __BOND_TRANS_EXCEPT
    global __BOND_BUFFERS, __BOND_CHANNELS

    if proto == "PICKLE":
        __BOND_PROTO = __BOND_PICKLE
    elif proto == "JSON":
        __BOND_PROTO = __BOND_JSON
    else:
        raise Exception('unknown protocol "{proto}"'.format(proto=proto))

    sys.stdout = __BOND_BUFFERS['STDOUT']
    sys.stderr = __BOND_BUFFERS['STDERR']
    sys.stdin = open(os.devnull)

    __BOND_TRANS_EXCEPT = trans_except
    __BOND_sendstate("ready".upper())
    ret = __BOND_repl()
    __BOND_sendstate("BYE")
    exit(ret)
