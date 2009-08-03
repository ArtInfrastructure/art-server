from datetime import datetime
import xml.dom.minidom
from xml.dom.minidom import Node

# 2009-08-03 10:23:51.771608
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

class SnapshotList:
	"""A list of snapshot information in the form (timestamp, url)"""
	def __init__(self, xml_data):
		doc = xml.dom.minidom.parseString(xml_data)
		self.snapshots = []
		for node in doc.getElementsByTagName("snapshot"):
			timestamp = datetime.strptime(node.getAttribute('timestamp').split('.')[0], TIMESTAMP_FORMAT)
			self.snapshots.append((timestamp, node.getAttribute('url')))
	def __getitem__(self, key): return self.snapshots[key]
	def __setitem__(self, key, item): self.snapshots[key] = item
	def __len__(self): return len(self.snapshots)
	def __delitem__(self, key): del self.snapshots[key]
	def append(item): self.snapshots.append(item)
	def extend(item): self.snapshots.extend(item)
	def insert(index, item): self.snapshots.insert(index, item)
	def remove(item): self.snapshots.remove(item)
	def pop(index=None): self.snapshots.pop(index)
	def index(item): self.snapshots.index(item)
	def count(): self.snapshots.count()
	def sort(): self.snapshots.sort()
	def reverse(): self.snapshots.reverse()


