import gtk

class Document(gtk.TextView):
	"""Class Documents creates GtkTextView widget, which maintains text processing functions."""
	def __init__(self, handler, bg, fontColor, text):
		super(Document, self).__init__()
		self.handler = handler
		self.buffer = gtk.TextBuffer()
		self.set_buffer(self.buffer)
		self.set_style(bg, fontColor)
		self.buffer.set_text(text)
		self.set_left_margin(5)
		self.buffer.connect('changed', self.handler.set_numbers)
		self.buffer.connect('changed', self.handler.toolbar.activate_actions)
		self.clipboard = gtk.Clipboard()
		#self.set_clipboard(self.c
		self.lastSaved = self.get_text()
		
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
