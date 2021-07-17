import socket
import requests
import threading
import eventlet
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

finame = raw_input("Enter filename: ")
fol = raw_input("Enter a folder to save report[default: .]: ")
listip = []

def genReport(name):
	global link
	global fol
	fname = "{}/{}_http.txt".format(fol,name)
	f = open(fname,'w')
	data = ""
	for x in link:
		form = "{}\t{}\t{}\t{}\n".format(x[0],x[2],x[1],x[4])
		data += form
	f.write(data)
	f.close()
	print "[+] Data has been saved to filename: {}".format(fname)

def genIP(name):
	global link
	global fol
	fname = "{}/{}_iphttp.txt".format(fol,name)
	f = open(fname,'w')
	data = ""
	for x in listip:
		form = "{}\n".format(x)
		data += form
	f.write(data)
	f.close()
	print "[+] Data ip has been saved to filename: {}".format(fname)
fet = 0

count =1
def get_domain(url):
	headers= {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/json;charset=utf-8"
}
	ln = "https://decoder.link/sslchecker/{}/443".format(url)
	r = requests.get(url=ln, headers=headers)
	headers = r.headers
	text = r.content
	text = text.split("Server certificate")
	text = text[1].split('\n')
	text = text[1].split('CN=')
	print "{} - {}".format(text[1],url)
	return text[1]
# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
link = []
eventlet.monkey_patch()
def get_status(url,hitung):
    global fet
    ln = "http://{}".format(url)
    ip = "-"
    try:
	ip = socket.gethostbyname(url)
    except:
	ip = "-"

    try:
	#with eventlet.Timeout(10):
       	req = requests.get(ln,verify=False,timeout=60)
	soup = BeautifulSoup(req.text,'html.parser')
	title = "Please Check"
	title = soup.title
	if title is None:
		title = "Kosong"
	else:
		title = title.string
		title = title.strip().encode('utf8')
#        print req.status_code
	#web = get_domain(url)
#	web = get_domain(url)
        result = [url,req.status_code,title,hitung,ip]
	link.append(result)
	if ip not in listip:
		listip.append(ip)
	#print "[INFO]: Data {} Inputted".format(hitung)
	fet+=1
        print "[INFO]: {} is UP with {} response code!".format(url,req.status_code)
    except:
	print "[-]{}".format(url)
	sc = "Failed"
	ttl = "None"
	result = [url,sc,ttl,hitung,ip]
	link.append(result)
	pass
#        print "[ERROR]: {} is not UP error".format(url)
#        print "[-]: {}".format(url)
def sortSecond(val):
    return val[3]

url = []
#READ FILE
filename = finame
with open(filename) as f:
    content = f.read().splitlines()

for line in content:
    url.append(line)

print "[INFO]: Loaded {} Data from file {}.".format(len(url),filename)

threadshttp = []
threadshttps = []

for x in url:
    linkhttp = "http://{}".format(x)
    linkhttps = "https://{}".format(x)
    #thttp = threading.Thread(target=get_status,args=(linkhttp,))
    thttps = threading.Thread(target=get_status,args=(x,count,))
    count +=1
    #threadshttp.append(thttp)
    threadshttps.append(thttps)

for x in threadshttps:
    x.start()
for x in threadshttps:
    x.join()

print "[INFO]: {} Fetched Data,{} is UP".format(count-1,fet)
link.sort(key = sortSecond, reverse = False)
for x in link:
    print "{} {}-[{}]".format(x[0],x[1],x[2])

genReport(finame)
genIP(finame)
