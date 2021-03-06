import os
from eventlet.green import subprocess
from hcloud.exceptions import Error
import shlex

def cmd_run(cmd):
    _pipe = subprocess.PIPE
    obj = subprocess.Popen(cmd, stdin=_pipe,
                           stdout=_pipe,
                           stderr=_pipe,
                           env=os.environ,
                           shell=True)
    result = obj.communicate()
    obj.stdin.close()
    _returncode = obj.returncode
    return _returncode, result

def execute_command(cmdstring, cwd=None, preexec_fn=None, env=None, shell=False):
    if shell:
        cmdstring_list = cmdstring
    else:
        cmdstring_list = shlex.split(cmdstring)

    sub = subprocess.Popen(cmdstring_list, cwd=cwd, preexec_fn=preexec_fn, env=env, stdin=subprocess.PIPE,stdout=subprocess.PIPE, shell=shell, bufsize=4096)
    output, err = sub.communicate()
    return int(sub.returncode), output, err

def write_to_file(file, str_config):
    try:
        with open(file, "w") as fobj:
            fobj.write(str_config)
    except Exception,err:
        errmsg = "Write to file error: %s" % err
        raise Error(str(errmsg))