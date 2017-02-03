#!/usr/bin/python

#import Gtk
from gi.repository import Gtk, Gio, GObject

class LineNumbers(Gtk.TextView):
	"""Class Documents creates GtkTextView widget, which maintains text processing functions."""
	def __init__(self, handler, doc, bg, fontColor):
		super(LineNumbers, self).__init__()
		self.set_can_focus(False)
		self.set_editable(False)
		self.set_cursor_visible(False)
		context = self.get_style_context()
		#context.set_background(Gtk.STYLE_PROPERTY_BACKGROUND_COLOR)
		
		self.doc = doc
		self.set_right_margin(5)
		self.set_left_margin(5)
		self.buffer = Gtk.TextBuffer()
		self.set_buffer(self.buffer)
		self.set_style(bg, fontColor)
		self.set_numbers()
		
	def set_numbers(self):
		max_num = self.doc.buffer.get_line_count()
		self.buffer.set_text('')
		for num in range(max_num):
			self.buffer.insert(self.buffer.get_end_iter(), '%d \n' % num)
			
	def set_style(self, bg, fontColor):
		#self.modify_base(Gtk.StateType.NORMAL, Gtk.gdk.Color(bg))
		#self.modify_text(Gtk.StateType.NORMAL, Gtk.gdk.Color(fontColor))
		pass
		
