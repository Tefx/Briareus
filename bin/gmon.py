#!/usr/bin/env python

import sys
sys.path.append("/usr/local/lib/python2.7/site-packages/")
sys.path.append("..")
sys.path.append('../../Thinkpol')

from PySide.QtCore import QThread, Signal, QObject, QFile, QTimer
from PySide.QtGui import QApplication, QTreeWidgetItem
from PySide.QtUiTools import QUiLoader

from Thinkpol import Agent
from sys import argv
from time import sleep

def beautiful_mem(s):
	cl = [' B', ' KB', ' MB', ' GB', ' TB']
	i = 0
	while s > 1024:
		s = round(s/1024, 1)
		i += 1
	return str(s)+cl[i]

def beautiful_percent(s):
	return str(round(s*100, 2))


class Backend(QThread):
	nodesReady = Signal(dict)

	def __init__(self, agent):
		QThread.__init__(self)
		self.agent = agent

	def run(self):
		while True:
			nodes = self.agent.fetch()
			print nodes
			self.nodesReady.emit(nodes)
			sleep(5)


class GuiProxy(QObject):
	def __init__(self, ui_file, agent):
		self.agent = agent
		loader = QUiLoader()
		f = QFile(ui_file)
		f.open(QFile.ReadOnly)
		self.widget = loader.load(f)
		f.close()
		self.backend = Backend(agent)
		self.backend.nodesReady.connect(self.update)
		self.backend.start()
		self.widget.show()

	def update(self, nodes):
		self.update_tree(nodes)
		self.update_cpu_info(nodes)
		self.update_mem_info(nodes)

	def update_cpu_info(self, nodes):
		total_ut = sum([v['user_time'] for k,v in nodes.iteritems()])
		total_st = sum([v['sys_time'] for k,v in nodes.iteritems()])
		total_it = sum([v['idle_time'] for k,v in nodes.iteritems()])
		total_t = total_ut + total_st + total_it

		self.widget.userPerLable.setText(beautiful_percent(total_ut/total_t))
		self.widget.sysPerLable.setText(beautiful_percent(total_st/total_t))
		self.widget.idlePerLable.setText(beautiful_percent(total_it/total_t))

		num_cpus = sum([v['num_cpus'] for k,v in nodes.iteritems()])
		self.widget.cpuNumLable.setText(str(num_cpus))

		num_works = 0
		for k,v in nodes.iteritems():
			for kw, vw in v['worker_info'].iteritems():
				if vw['status'] == 'running':
					num_works += 1
		self.widget.workNumLable.setText(str(num_works))

		self.widget.nodeNumLable.setText(str(len(nodes)))

	def update_mem_info(self, nodes):
		vm_total = sum([v['vm_total'] for v in nodes.itervalues()])
		vm_available = sum([v['vm_available'] for v in nodes.itervalues()])
		vm_used = sum([v['vm_used'] for v in nodes.itervalues()])
		vm_active = sum([v['vm_active'] for v in nodes.itervalues()])
		vm_inactive = sum([v['vm_inactive'] for v in nodes.itervalues()])
		vm_cached = sum([v['vm_cached'] for v in nodes.itervalues()])

		self.widget.totalMemLable.setText(beautiful_mem(vm_total))
		self.widget.availMemLable.setText(beautiful_mem(vm_available))
		self.widget.usedMemLable.setText(beautiful_mem(vm_used))
		self.widget.activeMemLable.setText(beautiful_mem(vm_active))
		self.widget.inactiveMemLable.setText(beautiful_mem(vm_inactive))
		self.widget.cachedMemLable.setText(beautiful_mem(vm_cached))


	def update_tree(self, nodes):
		self.widget.treeWidget.clear()
		for k,v in nodes.iteritems():
			node = QTreeWidgetItem(self.widget.treeWidget)
			node.setText(0, str(k))
			node.setText(1, str(v['cpu_percent']))
			node.setText(2, str(v['vm_percent']))
			node.setText(4, beautiful_mem(v['vm_used']))
			node.setText(5, beautiful_mem(v['vm_total']))
			for kw, vw in v['worker_info'].iteritems():
				worker = QTreeWidgetItem(node)
				worker.setText(0, str(kw))
				worker.setText(1, str(vw['cpu_percent']))
				worker.setText(2, str(vw['memory_percent']))
				worker.setText(3, str(vw['status']))
				worker.setText(4, beautiful_mem(vw['memory_info'][0]))
				worker.setText(5, beautiful_mem(vw['memory_info'][1]))
		self.widget.treeWidget.expandAll()


if __name__ == '__main__':
	app = QApplication(argv)
	smith = Agent(("210.72.68.189", 10001))
	gui = GuiProxy("gmon.ui", smith)
	sys.exit(app.exec_())