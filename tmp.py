import subprocess
target = 'ping 127.0.0.1 -c 5'

def check_output(target):
    process1 = subprocess.Popen(target, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        line = process1.stdout.readline()
        if not line:
            break
        print line.rstrip()