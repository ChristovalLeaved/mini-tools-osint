import os,sys
import argparse
from concurrent.futures import ThreadPoolExecutor

pr = argparse.ArgumentParser(prog="python ports.py")
pr.add_argument("-f", metavar="file", help="scanning ip")

args = pr.parse_args()
arglen = len(sys.argv)

listip = []

def run(x):
    os.system("python port.py -ip {}".format(x))

if args.f and arglen == 3:
    with open(args.f) as f:
        content = f.read().splitlines()

    for line in content:
        listip.append(line)
    
    print "[INFO]: Loaded {} Data from file {}.".format(len(listip),args.f)
    pool = ThreadPoolExecutor(max_workers=1)
    for x in listip:
        pool.submit(run,x)
    pool.shutdown(wait=True)

else:
    print pr.print_help()

