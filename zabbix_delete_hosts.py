#!/usr/bin/env python
#!/usr/bin/python -u
import json
import urllib2
import sys

url = 'http://10.13.1.64//zabbix/api_jsonrpc.php'
#url = 'http://10.13.4.84//zabbix/api_jsonrpc.php'
zabbixUserUI="Admin"
zabbixPassword="zabbix"

obj = {"jsonrpc": "2.0","method": "user.login","params": {"user": zabbixUserUI,"password": zabbixPassword},"id": 0}
data = json.dumps(obj)
request = urllib2.Request(url, data, {'Content-Type': 'application/json'})
response = urllib2.urlopen(request)
res = json.load(response)

hash_pass=[]
if 'error' in res:
        # An error occurred; raise an exception
        print 'An error occurred! %s' %res["error"]
        sys.exit(-1)
try:
        hash_pass=res["result"]
        #print hash_pass
except:
        hash_pass=res["error"]["data"]
        print hash_pass
        sys.exit()
#print "Auth token is %s" %(hash_pass)

def deletehost(hostid):

	"""Function which deletes the host from zabbix"""

	#print "hostid to delete",hostid
        obj3 = {"jsonrpc": "2.0","method": "host.delete","params": hostid,"auth": hash_pass,"id": 2}
        data3 = json.dumps(obj3)
        request3 = urllib2.Request(url, data3, {'Content-Type': 'application/json'})
        response3 = urllib2.urlopen(request3)
        res3 = json.load(response3)

def checkhost(hostname):

	"""Check if the host exist in zabbix to delete"""

	#print "checking hostname",hostname
	for host in hostname:
		#print "host is",host
		obj4 = {"jsonrpc": "2.0","method": "host.exists","params": {"host": host},"auth": hash_pass,"id": 3}
		data4 = json.dumps(obj4)
		request4 = urllib2.Request(url, data4, {'Content-Type': 'application/json'})
		response4 = urllib2.urlopen(request4)
		res4 = json.load(response4)
		#print "hostname check results - ",res4["result"]
		if res4["result"] != True:
			print "%s - This host doesn't exist in zabbix" %(host)

def gethostid(hostname):

	"""Get host ID from hostname"""

	#print "hostnames to delete",hostname
	checkhost(hostname)
	obj2 = {"jsonrpc": "2.0","method": "host.get","params": {"output": "extend","filter": {"host":hostname}},"auth": hash_pass,"id": 1}
	data2 = json.dumps(obj2)
	request2 = urllib2.Request(url, data2, {'Content-Type': 'application/json'})
	response2 = urllib2.urlopen(request2)
	res2 = json.load(response2)
	hostid=[]
	for i in range(len(res2["result"])):
		hostid.append(res2["result"][i]["hostid"])
	deletehost(hostid)

def main():
	if len(sys.argv) < 2:
		print "The script takes in atleast 1 hostname as arguement, multiple hostnames can be entered with space"
		print "Example:", "zabbix_delete_hosts.py hostname1"
	else:
		gethostid(sys.argv[1:])

if __name__ == '__main__':
	main()
