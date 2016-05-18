### bond Python interface loader
### NOTE: use ### for comments *only*, as this code is reduced as much as
###       possible to be injected into the interpreter *without parsing*.

def __BOND_stage1():
    import sys, json
    sys.stdout.write("stage2\n".upper())
    sys.stdout.flush()
    line = sys.stdin.readline().rstrip()
    stage2 = json.loads(line)
    exec(stage2['code'], globals())
    __BOND_start(*stage2['start'])

__BOND_stage1()
