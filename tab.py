import gtk, textview, lines

class Tab():
	def __init__(self, handler, label, text):
		self.handler = handler
		self.label = label
		self.text = text
		self.doc = textview.Document(handler, handler.get_option('textview_bg'), handler.get_option('textview_font_color'), text)
		self.lineNumbers = lines.LineNumbers(handler, self.doc, handler.get_option('lines_bg'), handler.get_option('lines_font_color'))
		self.handler.toolbar.deactivate_actions()
		
	def set_tab_layout(self):
		hbox = gtk.HBox()
		gtkLabel = gtk.Label(self.label)
		button = gtk.Button(gtk.STOCK_CLOSE)
		hbox.pack_start(gtkLabel, False, False, 0)
		hbox.pack_start(button, False, False, 0)
		hbox.show_all()
		return hbox

	def set_content(self):
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		hbox = gtk.HBox()
		hbox.pack_start(self.lineNumbers, False, False, 0)
		hbox.pack_start(self.doc)
		sw.add_with_viewport(hbox)
		return sw
		
