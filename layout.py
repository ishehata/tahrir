#!/usr/bin/python

#import Gtk
from gi.repository import Gtk, Gio, GObject

class Layout(Gtk.Box):
	"""class Layout() holds the main design of the text editor."""
	
	def __init__(self, handlerClass):
		"""Constructs instance of Layout()."""
		super(Layout, self).__init__()
		self.set_property('orientation', Gtk.Orientation.VERTICAL)
		self.handler = handlerClass
		self.init_layout()
		self.show_all()
		
	def init_layout(self):
		toolbarPosition = self.get_toolbar_position()
		if toolbarPosition == 'top':
			self.pack_start(self.handler.toolbar, False, False, 0)
			self.pack_start(self.handler.tabbar, True, True, 0)
		elif toolbarPosition == 'bottom':
			self.pack_start(self.handler.tabbar, True, True, 0)
			self.pack_start(self.handler.toolbar, False, False, 0)
		
		
	def get_toolbar_position(self):
		toolbarPosition = self.handler.get_option('toolbar_position')
		return toolbarPosition
		
	
