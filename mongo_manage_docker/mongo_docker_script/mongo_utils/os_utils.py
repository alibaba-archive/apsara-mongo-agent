

import time
import os
import sys
import pwd
import errno
import subprocess


def exec_command(cmd, timeout=180):
    def get_interval_iter():
        """a interval iterator"""
        MIN_INTERVAL, MAX_INTERVAL = 0.1, 1
        while True:
            yield min(MIN_INTERVAL, MAX_INTERVAL)
            if MIN_INTERVAL < MAX_INTERVAL:
                MIN_INTERVAL *= 2
    interval_iter = get_interval_iter()
    start_time = time.time()
    deadline = start_time + timeout
    close_fds = False if os.name == 'nt' else True
    pipe = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=close_fds)
    pipe_fd = pipe.stdout.fileno()
    # return the integer 'file descriptor' used by the underlying implementation
    if os.name == 'nt':
        # get the file handler of windows platform to call win32 API
        import msvcrt
        pipe_fd = msvcrt.get_osfhandle(pipe_fd)
    else:
        # set the file to Nonblock file
        import fcntl
        fcntl.fcntl(pipe_fd, fcntl.F_SETFL, os.O_NONBLOCK)
    output = ''
    if timeout:
        while time.time() < deadline:
            if pipe.poll() is not None:
                output += pipe.stdout.read()
                print 'during time: %s' % (time.time()-start_time)
                return pipe.returncode, output
            if os.name == 'nt':
                import ctypes.wintypes
                c_avail = ctypes.wintypes.DWORD()
                # get the number of data in pipe
                ctypes.windll.kernel32.PeekNamedPipe(pipe_fd, None, 0, None, ctypes.byref(c_avail), None)
                #print (pipe_fd, c_avail)
                # read all data of pipe in each second to avoid pipe to overflow
                if c_avail.value:
                    output += pipe.stdout.read(c_avail.value)
                else:
                    interval = next(interval_iter)
                    time.sleep(interval)
            else:
                # select function wait until pipe_fd is ready for reading
                import select
                rlist, _, _ = select.select([pipe_fd], [], [], next(interval_iter))
                if rlist:
                    try:
                        output += pipe.stdout.read(1024)
                    except IOError as e:
                        if e[0] != errno.EAGAIN:
                            raise
                        sys.exc_clear()
        pipe.stdin.close()
        pipe.stdout.close()
        try:
            pipe.terminate()
        except OSError as e:
            if e[0] != 5:
                raise
            for _ in range(10):
                try:
                    os.kill(pipe.pid, 9)
                except OSError as e:
                    if e[0] in (3, 87):
                        break
                    else:
                        time.sleep(1)
            else:
                print 'the process cannot be killed: %s' % cmd
        return 0x7f, 'time out'
    else:
        pipe.wait()
        return pipe.returncode, pipe.stdout.read()

def chown_paths(path_list, user, group):
    for path in path_list:
        if os.path.exists(path):
            cmd = "chown -R %s:%s %s" % (user, group, path)
            status, stdout = exec_command(cmd)
            if status != 0:
                print "%s ERROR: %s" % (cmd, stdout)
                sys.exit(-1)

            print "Run: %s" % cmd
        else:
            print "ERROR: The path %s is not exist!" % path
            sys.exit(-1)

def add_os_user(user, group):
    print "Add system user %s to group %s" % (user, group)
    try:
        pwd_struct = pwd.getpwnam(user)
        print "The user %s exists, go on!" % user
    except:
        status, stdout = exec_command("groupadd %s" % group)
        if status != 0:
            print "ERROR: we can not add the group!"
            sys.exit(-1)
        status, stdout = exec_command("useradd %s -g %s" % (user, group))
        if status != 0:
            print "ERROR: we can not create the user!"
            sys.exit(-1)
