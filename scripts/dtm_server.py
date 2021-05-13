import os
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
from time import sleep
import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl

dirname, filename = os.path.split(os.path.abspath(__file__))
posts_received = 0
post_data = ''

def appendLog(dcm_temperature, dcm_timestamp):
	"""update the .xml log of dcm updates every 1 minute
	"""
	if posts_received % 12 == 0:  # because the http client program running on the dcm
		# submits a POST request every 5 seconds
		tree = ET.parse('TrustLogv2.xml')  # create xml tree from file contents
		root = tree.getroot()  # ID root of tree (TrustLog)
		dtm_time = str(datetime.datetime.now())  # get timestamp of this moment
		newContact = ET.SubElement(root, 'DCMContact')  # add element (instance of DCM contacting DTM) to the tree
		newContact.set('DCM_timestamp', dcm_timestamp)  # time from xml sent from DCM in POST
		newContact.set('DCM_temp', dcm_temperature)  # temp from xml sent from DCM in POST
		newContact.set('log_update_timestamp', dtm_time)  # DTM time
		prettyXmlStr = prettify(root)  # new string made using prettify()
		prettyXmlStr = prettyXmlStr.replace('</TrustLog>',
											'\n</TrustLog>')  # Re-newline the tree close
		prettyXmlStr = prettyXmlStr.replace('<TrustLog>',
											'\n<TrustLog>')  # re-newline the tree open, the prettify() strips them for some reason
		with open('TrustLogv2.xml', 'w') as logFile:  # open log and write
			print(prettyXmlStr, file=logFile)


def prettify(elem):
	"""Return a pretty-printed XML string for the Element.
	"""
	rough_string = ET.tostring(elem, 'utf-8')  # encode xml object as bytes
	new_rough_string = rough_string.replace(b'\n',
											b'')  # otherwise the ElementTree methods add newlines to the whole file each log update
	new_rough_string = rough_string.replace(b'\t',
											b'')  # the b'' is because this is a <class 'bytes'> not <class 'string'>
	reparsed = minidom.parseString(new_rough_string)  # takes bytes as arg, produces Document object
	return reparsed.toprettyxml(indent='\t', newl='')  # returns a string, the args are super finnicky


def getDCMTemp(xml_input):
	"""Return the DCM temp as float from the parsed xml msg
	"""
	root = ET.fromstring(xml_input)
	DCMTemp = root[0]  # root[0] is the DCMUpdate
	temp = float(DCMTemp.attrib[
					 'temp'])  # DCMTemp.attrib['temp'] returns the attribue matching key 'temp', then convert to float
	return temp


def getDCMTime(xml_input):
	"""Return the DCM time as string from the parsed xml msg
	"""
	root = ET.fromstring(xml_input)
	DCMTime = root[0]  # DCMContact[0] is update
	timestamp = str(DCMTime.attrib[
						'timestamp'])  # DCMTemp.attrib['timestamp'] returns the attribue matching key 'temp', then convert to float
	return timestamp


def makeHtmlLine(str_in):
	"""add formatting for a "paragraph" in html to a string
	"""
	str_in = '<p style="text-indent: 40px">' + str_in + '</p>'
	return str_in


def makeHtmlText(str_in):
	"""add formatting for an html textarea to a string
	"""
	str_in = '<textarea rows="2" cols="100" style="border:double 2px blue;">' + str_in + '</textarea>'
	return str_in


class MyServer(BaseHTTPRequestHandler):
	"""server derived from python standard library BASEHTTPRequestHandler object, custom handlers
		for HEAD, GET, POST, and redirect interactions
	"""

	def do_HEAD(self):
		"""HEAD method type, sends to client
		"""
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()  # need to call end_headers() to actually send the headers

	def _redirect(self, path):
		"""redirect method type
		"""
		self.send_response(303)
		self.send_header('Content-type', 'text/html')
		self.send_header('Location', path)
		self.end_headers()

	def do_GET(self):
		"""GET method type, updates the "served" html page that you can access from a browser
			on a local network with [ip address 00.00.00.00 blah]:[port num, 4 digits, matching encoded]
			copy pasted to url in browser
		"""
		print("do_GET called")
		self.do_HEAD()  # call the HEAD method, which sends headers to the client

	def do_POST(self):
		"""POST method type
			the http.client is running on a DCM on the network, that client
			submits requests with 'POST', which contain xml
			rfile.read().decode() then decodes that msg
			and saves it to a global string var
		"""
		global posts_received  # global keyword needed to modify the var, there were errors declaring as
		# class data members
		global post_data
		posts_received += 1  # iterate count of POST requests received
		print("someone knocked on this post door")
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length).decode("utf-8")  # Get the data
		#self.do_HEAD()
		print(" POST REQUEST RECEIVED. raw content:")
		print(post_data)
		print(posts_received)



"""
this is main, just run the server
"""
if __name__ == '__main__':
    host_port = 4430
    if (len(sys.argv) > 1):
        host_port = host_port + int(sys.argv[1])
    host_name = 'localhost'  # DTM Rpi address
    key_path = dirname + '/certs/private/server.key'
    cert_path = dirname + '/certs/server.crt'
    http_server = HTTPServer((host_name, host_port), MyServer)
    http_server.socket = ssl.wrap_socket(http_server.socket, keyfile=key_path, certfile=cert_path, server_side=True)
    print("Simple Printing SERVER RUNNING ON DTM RASPBERRY PI")
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()