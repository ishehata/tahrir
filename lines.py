import gtk

class LineNumbers(gtk.TextView):
	"""Class Documents creates GtkTextView widget, which maintains text processing functions."""
	def __init__(self, handler, doc, bg, fontColor):
		super(LineNumbers, self).__init__()
		self.set_can_focus(False)
		self.set_editable(False)
		self.set_cursor_visible(False)
		self.doc = doc
		self.set_right_margin(5)
		self.buffer = gtk.TextBuffer()
		self.set_buffer(self.buffer)
		self.set_style(bg, fontColor)
		self.set_numbers()
		
	def set_numbers(self):
		max_num = self.doc.buffer.get_line_count()
		self.buffer.set_text('')
		for num in range(max_num):
			self.buffer.insert(self.buffer.get_end_iter(), '%d \n' % num)
			
	def set_style(self, bg, fontColor):
		self.modify_base(gtk.STATE_NORMAL, gtk.gdk.Color(bg))
		self.modify_text(gtk.STATE_NORMAL, gtk.gdk.Color(fontColor))
