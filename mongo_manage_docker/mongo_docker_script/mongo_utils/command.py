import os
import time
import subprocess


def execute_command(cmd, timeout=600):
    def get_interval_iter():
        MIN_INTERVAL, MAX_INTERVAL = 0.1, 1
        while True:
            yield min(MIN_INTERVAL, MAX_INTERVAL)
            if MIN_INTERVAL < MAX_INTERVAL:
                MIN_INTERVAL *= 2
    interval_iter = get_interval_iter()
    start_time = time.time()
    close_fds = False if os.name == 'nt' else True
    pipe = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            close_fds=close_fds)

    if timeout:
        while timeout > 0:
            if pipe.poll() is not None:
                print "during time: %s" % (time.time() - start_time)
                return pipe.returncode, pipe.stdout.read()
            else:
                interval = next(interval_iter)
                timeout -= interval
                time.sleep(interval)
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

        return 0x7f, 'timed out'
    else:
        pipe.wait()
        return pipe.returncode, pipe.stdout.read()

