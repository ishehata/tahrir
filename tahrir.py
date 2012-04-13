import gtk, handler, layout

class Maximus(gtk.Window):
	"""Maximus is a neat,simple and elegant text editor."""
	
	def __init__(self):
		"""Constructs instance of Tahrir."""
		super(Maximus, self).__init__()		
		self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.windowTitle = 'Maximus'
		self.set_title(self.windowTitle)
		self.resize(700,550)
		self.connect('delete-event', self.on_delete_event)
		self.init_comp()
		self.show_all()
		last_tab = self.handler.tabbar.get_nth_page(-1)
		self.handler.tabbar.docs[-1].grab_focus()
		
	__gsignals__ = {
		"delete-event" : "override"
	}
		
	def init_comp(self):
		self.handler = handler.Handler(self)
		self.layout = layout.Layout(self.handler)
		self.add(self.layout)
		
	def on_delete_event(event, self, widget):
		#self.handler.tabbar.set_current_page(-1)
		#for i in self.handler.tabbar.docs:
			#tab = self.handler.tabbar.get_current_page()
		#	self.handler.tabbar.close_tab_by_id(tab)
			#tab = self.handler.tabbar.prev_page()
		#self.handler.tabbar.set_current_page(0)
		#for i in range(0, tabsNumber):
			#doc = self.handler.tabbar.docs[i]
			#lines = self.handler.tabbar.lineNumbers[i]
			#self.handler.tabbar.close_tab(doc, lines)
		self.hide()
		self.destroy_app()
		return True
			
#			if self.handler.tabbar.get_n_pages() == 0:
#				self.destroy_app()
				
	def destroy_app(self):
		gtk.main_quit()	
		
Maximus()
gtk.main()
