import gtk

class Document(gtk.TextView):
	"""Class Documents creates GtkTextView widget, which maintains text processing functions."""
	def __init__(self, handler, bg, fontColor, text):
		super(Document, self).__init__()
		self.handler = handler
		self.tagTable = gtk.TextTagTable()
		self.buffer = gtk.TextBuffer(self.tagTable)
		self.buffer.set_modified(False)
		self.set_buffer(self.buffer)
		self.set_style(bg, fontColor)
		self.buffer.set_text(text)		
		self.set_left_margin(5)
		self.boldBlue = self.buffer.create_tag('boldBlue')
		self.boldBlue.set_property('foreground', 'blue')
		self.do_highlight(None)
		self.buffer.connect('changed', self.handler.set_numbers)
		self.buffer.connect('changed', self.do_highlight)
		self.buffer.connect('changed', self.set_buffer_modified)
		#self.buffer.connect('modified_changed', self.handler.toolbar.activate_actions)
		
		self.clipboard = gtk.Clipboard()
		self.searchTag = self.buffer.create_tag('yellowBackground')
		self.searchTag.set_property('background', 'yellow')
		
		
	def set_buffer_modified(self, widget):
		self.buffer.set_modified(True)
		self.handler.toolbar.activate_save_button()
		
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
		inBoldBlue = ['def', 'if', 'True', 'for', 'False', 'While', 'pass', 'break', 'return', 'elif', 'else']
		for term in inBoldBlue:
			result = self.find_text(term)
			if result:
				for iter in result:
					self.buffer.apply_tag(self.boldBlue, iter[0], iter[1])
				
		
	def set_style(self, bg, fontColor):
		self.modify_base(gtk.STATE_NORMAL, gtk.gdk.Color(bg))
		self.modify_text(gtk.STATE_NORMAL, gtk.gdk.Color(fontColor))
		
	def get_text(self):
		text = self.buffer.get_text(self.buffer.get_start_iter(), self.buffer.get_end_iter())
		return text
		
	def has_unsaved_changes(self):
		text = self.get_text()
		if text == self.lastSaved:
			return False
		elif text != self.lastSaved:
			return True
			
	def cut_text(self):
		self.buffer.cut_clipboard(self.clipboard, self.get_editable())
	
	def copy_text(self):
		self.buffer.copy_clipboard(self.clipboard)
	
	def paste_text(self):
		self.buffer.paste_clipboard(self.clipboard, None, self.get_editable())

	
