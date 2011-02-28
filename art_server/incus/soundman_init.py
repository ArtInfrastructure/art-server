"""
This script should be run once the machine running the SoundMan server has booted and the SoundMan service is running.

It will set up the interface and set the playback matrix to diagonal 1.

It will then iterate over all of the art server defined channel groups and set the gains accordingly.
"""
import traceback, sys, urllib, urllib2
from lxml import etree

from soundman_control import SoundManControl

def print_usage():
	print 'Usage:'
	print 'python soundman_init.py <soundman server IP#> <art server IP#>'

def get_resource(url):
	sock = urllib.urlopen(url)
	xml = sock.read()
	sock.close()
	return xml

def get_gains(incus_host, port=80):
	devices_xml = get_resource('http://%s:%s/api/audio/ab-device/' % (incus_host, port))
	parsed_xml = etree.fromstring(devices_xml)
	return [(channel.attrib['channel_type'], channel.attrib['number'], channel.attrib['gain']) for channel in parsed_xml.xpath('//abchannel')]
	
def main():
	if len(sys.argv) != 3:
		print_usage()
		return 1
	soundman_host = sys.argv[1]
	incus_host = sys.argv[2]
	print 'Initializing the SoundMan server at %s' % soundman_host
	soundman_control = SoundManControl(soundman_host)
	soundman_control.send_command('config set interface 0')
	soundman_control.send_command('set matrix pb diagonal gain 1;')

	for gain in get_gains(incus_host):
		soundman_control.set_gain('%s%s' % (gain[0], gain[1]), gain[2])

if __name__ == '__main__': main()
