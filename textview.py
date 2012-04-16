#!/usr/bin/python

#import Gtk
from gi.repository import Gtk, Gio, GObject

class Document(Gtk.TextView):
	"""Class Documents creates GtkTextView widget, which maintains text processing functions."""
	def __init__(self, handler, bg, fontColor, text):
		super(Document, self).__init__()
		self.handler = handler
		self.buffer = Gtk.TextBuffer()
		self.buffer.set_modified(False)
		self.set_buffer(self.buffer)
		self.set_style(bg, fontColor)
		self.buffer.set_text(text)		
		self.set_left_margin(5)
		self.boldBlue = self.buffer.create_tag('boldBlue')
		self.boldBlue.set_property('foreground', 'blue')
		self.boldBlue.set_property('weight', 700)
		self.green = self.buffer.create_tag('green')
		self.green.set_property('foreground', 'green')
		self.do_highlight(None)
		self.buffer.connect('changed', self.handler.set_numbers)
		self.buffer.connect('changed', self.do_highlight)
		self.buffer.connect('changed', self.set_modified)
		self.buffer.connect('changed', self.indicate_unsaved_changes)
		self.toUndo = []
		self.toRedo = []
		self.actions = Gtk.Clipboard()
		self.clipboard = Gtk.Clipboard()
		self.searchTag = self.buffer.create_tag('yellowBackground')
		self.searchTag.set_property('background', 'yellow')
		
		
	def set_modified(self, widgit):
		self.buffer.set_modified(True)
		self.toUndo.append(self.get_text())
		
	def undo(self):
		self.toRedo.append(self.get_text())
		toUndo = self.toUndo[-1]
		self.buffer.set_text(toUndo)
		#self.toUndo.del(-1)
		self.buffer.set_modified(True)
	
	def redo(self):
		self.buffer.set_text(self.toRedo.pop())
		self.buffer.set_modified(True)
		
	def has_unsaved_changes(self, widget):
		if self.buffer.get_modified() == True:
			return True
		else:
			return False
	
	def indicate_unsaved_changes(self, widget):
		if self.buffer.get_modified() == True:
			self.handler.toolbar.activate_save_button()
			self.handler.tabbar.set_tab_dirty()
		
	def search(self, parameter):
		self.buffer.remove_tag(self.searchTag, self.buffer.get_start_iter(), self.buffer.get_end_iter())
		start_iter = self.buffer.get_start_iter()
		result = self.find_text(parameter)
		if result:
			self.match_start = result[0][0]
			self.match_end = result[0][1]
			self.buffer.select_range(self.match_start, self.match_end)
			for word in result:
				match_start = word[0]
				match_end = word[1]
				self.buffer.apply_tag(self.searchTag, match_start, match_end)
		else:
			pass
	
	def search_forward(self, parameter):
		if self.match_end:
			start_iter = self.match_end
		if not self.match_end:
			start_iter = self.self.buffer.get_start_iter()
		found = start_iter.forward_search(parameter, 0, None)
		if found:
			self.match_start, self.match_end = found
			self.buffer.select_range(self.match_start, self.match_end)
			
	def search_backward(self, parameter):
		if self.match_end:
			start_iter = self.match_start
		if not self.match_start:
			start_iter = self.self.buffer.get_end_iter()
		found = start_iter.backward_search(parameter, 0, None)
		if found:
			self.match_start, self.match_end = found
			self.buffer.select_range(self.match_start, self.match_end)
			
	def find_text(self, parameter):
		start_iter = self.buffer.get_start_iter()
		result = []
		while True:
			found = start_iter.forward_search(parameter, 0, None)
			if found:
				match_start, match_end = found
				result.append((match_start, match_end))
				start_iter = match_end
			else:
				break
		return result
		
	def do_highlight(self, widget):
		self.iters = []
		start_iter = self.buffer.get_start_iter()
		inBoldBlue = ['def', 'if', 'True', 'for', 'False', 'While', 'pass', 'break', 'return', 'elif', 'else', 'class', 'import', 'self', 'while', 'do']
		for term in inBoldBlue:
			result = self.find_text(term)
			if result:
				for iter in result:
					self.buffer.apply_tag(self.boldBlue, iter[0], iter[1])
		for num in '0123456789':
			result = self.find_text(num)
			if result:
				for iter in result:
					self.buffer.apply_tag(self.green, iter[0], iter[1])
				
		
	def set_style(self, bg, fontColor):
		#self.modify_base(Gtk.STATE_NORMAL, Gtk.gdk.Color(bg))
		#self.modify_text(Gtk.STATE_NORMAL, Gtk.gdk.Color(fontColor))
		pass
		
	def get_text(self):
		text = self.buffer.get_text(self.buffer.get_start_iter(), self.buffer.get_end_iter())
		return text
		
			
	def cut_text(self):
		self.buffer.cut_clipboard(self.clipboard, self.get_editable())
	
	def copy_text(self):
		self.buffer.copy_clipboard(self.clipboard)
	
	def paste_text(self):
		self.buffer.paste_clipboard(self.clipboard, None, self.get_editable())

	
