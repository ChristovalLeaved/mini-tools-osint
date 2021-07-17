import socket
from concurrent.futures import ThreadPoolExecutor
import argparse,sys

pr = argparse.ArgumentParser(prog="python ports.py")
pr.add_argument("-ip", metavar="ip", help="scanning ip")

args = pr.parse_args()
arglen = len(sys.argv)

if args.ip and arglen ==3:
    remoteServer    = args.ip
    remoteServerIP  = socket.gethostbyname(remoteServer)
    thread = 300
    timeout = 10
    fol = "./port/"
else:
    pr.print_help()



# remoteServer    = raw_input("Enter a remote host to scan: ")
# remoteServerIP  = socket.gethostbyname(remoteServer)
# thread = int(raw_input("Enter a max thread: "))
# timeout = int(raw_input("Enter timeout time [>3]: "))
# fol = raw_input("Enter a folder to save report[default: .]: ")

success = []

def genReport(name):
    global success
    global fol
    fname = "{}/{}_port.txt".format(fol,name)
    f = open(fname,'w')
    data = ""
    for x in success:
	form = "IP: {}, Port: {}\n".format(x[0],x[1])
	data += form
    f.write(data)
    f.close()
    print "[+] Data has been saved to filename: {}".format(fname)

def checkPort(ip,port,count):
    if count % 100 == 0:
        print "[+] {} Port Loaded!".format(count)
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((ip,port))
    if result == 0:
	print ip,port
        data = [ip,port,count]
        success.append(data)
    sock.close()

def sort(val):
    return val[2]

def view():
    global success
    success.sort(key=sort,reverse = False)
    for x in success:
        print "[DATA] {} - {}".format(x[0],x[1])

pool = ThreadPoolExecutor(max_workers=thread)
for x in range(1,65536):
    pool.submit(checkPort,remoteServerIP,x,x)

pool.shutdown(wait=True)

view()
genReport(remoteServerIP)
