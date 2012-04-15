import gtk
import settings, toolbar, tabbar, textview, lines, getpass

class Handler():
	"""Class Handler() is the controller that handles most of the operations between Models."""

	def __init__(self, mainWindow):
		"""Constructs instance of Handler()."""
		self.mainWindow = mainWindow
		self.options = {}
		self.set_default_options()
		self.settings = settings.Settings(self)
		self.toolbar = toolbar.Toolbar(self)
		self.tabbar = tabbar.Tabbar(self)
		self.current_folder = ('/home/'+getpass.getuser())

		
	def on_click_new(self, widget):
		self.tabbar.create_new_tab()
	
	def on_click_open(self, widget):
		d = gtk.FileChooserDialog('Choose File', None, gtk.FILE_CHOOSER_ACTION_OPEN,
			(gtk.STOCK_CANCEL, 0, gtk.STOCK_OPEN, 1), None)
		d.set_default_response(1)
		d.set_current_folder(self.current_folder)
		if d.run() == 1:
			filePath = d.get_filename()
			filename = self.strip_filename(filePath)
			#self.mainWindow.set_window_title(filename)
			f = open(filePath, 'r')
			text = f.read()
			self.tabbar.create_new_tab(filename, text, filePath)
			self.tabbar.docs[-1].lastSaved = text
		self.current_folder = d.get_current_folder()
		d.destroy()
		
	def on_click_save(self, widget):
		tab_num = self.tabbar.get_current_page()
		self.save_doc(tab_num)
		
	def save_doc(self, tab_num):
		doc = self.tabbar.docs[tab_num]
		lineNumbers = self.tabbar.docs[tab_num]
		filePath = self.tabbar.files[tab_num]
		if filePath == None:
			d = self.save_dialog()
			response = d.run()
			if response == 1:
				filePath = d.get_filename()
				f = open(filePath, 'w')
				text = doc.get_text()
				f.write(text)
				f.close()
				doc.buffer.set_modified(False)
				self.current_folder = d.get_current_folder()
				self.toolbar.actions['save'].set_sensitive(False)
				self.tabbar.labels[tab_num].set_text(self.strip_filename(filePath))
				self.tabbar.files[tab_num] = filePath
			d.destroy()
		else:
			f = open(filePath, 'w')
			text = doc.get_text()
			f.write(text)
			f.close()
			doc.lastSaved = text
			self.toolbar.actions['save'].set_sensitive(False)
		
	def save_dialog(self):
		d = gtk.FileChooserDialog('Save Document', None, gtk.FILE_CHOOSER_ACTION_SAVE,
			(gtk.STOCK_CANCEL, 0, gtk.STOCK_SAVE, 1), None)
		d.set_current_folder(self.current_folder)
		d.set_default_response(1)
		return d
		
	def cut_text(self, widget):
		tab = self.tabbar.get_current_page()
		self.tabbar.docs[tab].cut_text()
		
	def copy_text(self, widget):
		tab = self.tabbar.get_current_page()
		self.tabbar.docs[tab].copy_text()
		
	def paste_text(self, widget):
		tab = self.tabbar.get_current_page()
		self.tabbar.docs[tab].paste_text()
		
	def strip_filename(self, filePath):
		filename = filePath.split('/')
		filename = filename[-1]
		return filename
		
	def set_numbers(self, widget):
		tab = self.tabbar.get_current_page()
		self.tabbar.lineNumbers[tab].set_numbers()
		
	def search_doc(self, parameter):
		tab = self.tabbar.get_current_page()
		doc = self.tabbar.docs[tab]
		doc.search(parameter)
		
	def search_forward(self, parameter):
		tab = self.tabbar.get_current_page()
		doc = self.tabbar.docs[tab]
		doc.search_forward(parameter)
		
	def search_backward(self, parameter):
		tab = self.tabbar.get_current_page()
		doc = self.tabbar.docs[tab]
		doc.search_backward(parameter)
		
	def prompt_save_dialog(self):
		d = gtk.MessageDialog(None,  gtk.DIALOG_MODAL,  gtk.MESSAGE_QUESTION, gtk.BUTTONS_NONE, None)
		d.add_button('Don\'t Save', -1)
		d.add_button('Cancel', 0)
		d.add_button('Save', 1)
		d.set_markup('There are unsaved changes, do you want to save them?')
		d.set_default_response(1)
		return d
		
	def set_default_options(self):
		"""Defines and sets the default options/preferences of the application."""
		self.options['toolbar_position'] = 'top'
		self.options['show_line_numbers'] = 'True'
		self.options['textview_bg'] = '#fff'
		self.options['textview_font_color'] = '#000'
		self.options['lines_bg'] = '#E3E3E3'
		self.options['lines_font_color'] = '#383737'
		
	def get_option(self, option_key):
		"""Returns values of the given option_key from options dictionary."""
		return self.options[option_key]
		
	def set_option(self, option_name, option_value):
		"""Sets option's value to the given parameter option_key."""
		self.options[option_key] = option_value
		
	def run_settings_dialog(self, data):
		self.settings.run()
		
	def set_show_line_numbers(self, data):
		if self.options['show_line_numbers'] == 'True':
			self.options['show_line_numbers'] = 'False'
			self.hide_line_numbers()
		elif self.options['show_line_numbers'] == 'False':
			self.options['show_line_numbers'] = 'True'
			self.show_line_numbers()
	
	def hide_line_numbers(self):
		for ln in self.tabbar.lineNumbers:
			ln.hide_all()
	
	def show_line_numbers(self):
		for ln in self.tabbar.lineNumbers:
			ln.show_all()
