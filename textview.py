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
		self.buffer.connect('changed', self.handler.set_numbers)
		self.buffer.connect('changed', self.code_highlight)
		self.buffer.connect('changed', self.set_buffer_modified)
		#self.buffer.connect('modified_changed', self.handler.toolbar.activate_actions)
		#self.do_highlight()
		self.clipboard = gtk.Clipboard()
		self.searchTag = gtk.TextTag()
		self.searchTag.set_property('background', 'red')
		self.tagTable.add(self.searchTag)
		self.codeTag = gtk.TextTag()
		self.tagTable.add(self.codeTag)
		self.codeTag.set_property('foreground', 'red')
		self.search_iter = self.buffer.get_start_iter()
		
	def code_highlight(self, widget):
		text = self.get_text()
		
		txt = text.split(' ')
		if 'def' in text:
			self.buffer.apply_tag(self.codeTag,self.buffer.get_start_iter(), self.buffer.get_end_iter())
		
	def set_buffer_modified(self, widget):
		self.buffer.set_modified(True)
		self.handler.toolbar.activate_save_button()
		
	def search(self, parameter):
		start_iter = self.buffer.get_start_iter()
		found = start_iter.forward_search(parameter, 0, None)
		if found:
			match_start, self.match_end = found
			self.buffer.select_range(match_start, self.match_end)
			#self.search_iter = match_end
		#if direction == 'forward':
		#	start_iter = end_iter
		#	self.find_text(start_iter, parameter)
	#	self.buffer.apply_tag(self.searchTag, self.buffer.get_start_iter(), self.buffer.get_end_iter())
	
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
			
	def find_text(self, start_iter, parameter):
		found = start_iter.forward_search(parameter, 0, None)
		while found:
			match_start, match_end = found
			self.buffer.select_range(match_start, match_end)
		return match_end
		
	def do_highlight(self, txt):
		tag = gtk.TextTag()
		print txt
		words = txt.split('/')
		for word in words:
			if word == 'def':
				tag.set_priority('foreground', 'red')
		self.tagTable.add(tag)
		
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

	
