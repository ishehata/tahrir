import gtk

class Toolbar(gtk.Toolbar):
	"""Class Toolbar() is a model for GtkToolbar, contains the main actions of the text editor."""
	
	def __init__(self, handler):
		"""Constructs instance of class Toolbar()."""
		super(Toolbar, self).__init__()
		self.handler = handler
		self.set_can_focus(False)
		self.actions = []
		self.init_actions()
		
		
		
	def init_actions(self):
		self.actions = {}
		#
		self.actions['new'] = gtk.ToolButton(gtk.STOCK_NEW)
		self.actions['new'].set_label('New Doc')
		self.actions['new'].set_tooltip_text('Create New Empty Document')
		self.actions['new'].connect('clicked', self.handler.on_click_new)
		self.insert(self.actions['new'], -1)
		#
		self.actions['open'] = gtk.ToolButton(gtk.STOCK_OPEN)
		self.actions['open'].set_label('Open Doc')
		self.actions['open'].set_is_important(True)
		self.actions['open'].set_tooltip_text('Open Document')
		self.actions['open'].connect('clicked', self.handler.on_click_open)
		self.insert(self.actions['open'], -1)
		#
		self.actions['save'] = gtk.ToolButton(gtk.STOCK_SAVE)
		self.actions['save'].set_label('Save Doc')
		self.actions['save'].set_tooltip_text('Save Document')
		self.actions['save'].set_sensitive(False)
		self.actions['save'].connect('clicked', self.handler.on_click_save)
		self.insert(self.actions['save'], -1)	
		#
		self.actions['separator'] = gtk.SeparatorToolItem()
		self.insert(self.actions['separator'], -1)
		#
		self.actions['undo'] = gtk.ToolButton(gtk.STOCK_UNDO)
		self.actions['undo'].set_tooltip_text('Undo')
		self.actions['undo'].set_sensitive(False)
		self.insert(self.actions['undo'], -1)
		#
		self.actions['redo'] = gtk.ToolButton(gtk.STOCK_REDO)
		self.actions['redo'].set_tooltip_text('Redo')
		self.actions['redo'].set_sensitive(False)
		self.insert(self.actions['redo'], -1)
		#
		self.actions['separator1'] = gtk.SeparatorToolItem()
		self.insert(self.actions['separator1'], -1)
		#
		self.actions['cut'] = gtk.ToolButton(gtk.STOCK_CUT)
		self.actions['cut'].set_tooltip_text('Cut text')
		self.actions['cut'].connect('clicked', self.handler.cut_text)
		self.insert(self.actions['cut'], -1)
		#
		self.actions['copy'] = gtk.ToolButton(gtk.STOCK_COPY)
		self.actions['copy'].set_tooltip_text('Copy text')
		self.actions['copy'].connect('clicked', self.handler.copy_text)
		self.insert(self.actions['copy'], -1)
		#
		self.actions['paste'] = gtk.ToolButton(gtk.STOCK_PASTE)
		self.actions['paste'].set_tooltip_text('Paste text')
		self.actions['paste'].connect('clicked', self.handler.paste_text)
		self.insert(self.actions['paste'], -1)
		#
		self.actions['spacer'] = gtk.ToolItem()
		self.actions['spacer'].set_expand(True)
		self.insert(self.actions['spacer'], -1)
		#
		self.actions['search'] = gtk.ToolItem()
		self.search_entry = gtk.Entry()
		self.actions['search'].add(self.search_entry)
		self.insert(self.actions['search'], -1)
		#
		self.actions['settings'] = gtk.ToolButton(gtk.STOCK_PREFERENCES)
		self.actions['settings'].set_tooltip_text('Adjust Settings')
		self.actions['settings'].connect('clicked', self.handler.run_settings_dialog)
		self.insert(self.actions['settings'], -1)

	def activate_actions(self, widget):
		self.actions['save'].set_sensitive(True)
		self.actions['undo'].set_sensitive(True)
		self.actions['redo'].set_sensitive(True)

		
	def deactivate_actions(self):
		self.actions['save'].set_sensitive(False)
		self.actions['undo'].set_sensitive(False)
		self.actions['redo'].set_sensitive(False)

