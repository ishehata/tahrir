#!/usr/bin/python

import textview, lines
from gi.repository import Gtk, Gio, GObject

class Tabbar(Gtk.Notebook):
	"""Class Tabbar() is a GtkNotebook, which contains tabs, textview and lines number inside it."""
	
	def __init__(self, handler):
		super(Tabbar, self).__init__()
		self.handler = handler
		self.set_can_focus(False)
		self.set_scrollable(True)
		self.set_show_border(False)
		#self.set_tab_pos(Gtk.Position.BOTTOM)
		self.docs = []
		self.lineNumbers = []
		self.labels = []
		self.strLabels = []
		self.files = []
		self.init_tab()
		self.connect('page-removed', self.set_actions_off)
		

	def init_tab(self):
		"""Constructs the very first tab"""
		self.create_new_tab()
		
	def set_actions_off(self, widget, child, page_num):
		tabs_num = self.get_n_pages()
		if tabs_num == 0:
			self.handler.toolbar.deactivate_save_button()
			self.handler.toolbar.deactivate_actions()
		else:
			pass
			
	def create_new_tab(self, label = 'Untitled Document', text='', filename=None):
		"""This functions adds a new tab to the GtkNotebook, the net tab has a GtkScrolledWindow as a child,
			which containes lines number and GtkTextView."""
		tab = Gtk.HBox()
		GtkLabel = Gtk.Label(label)
		self.labels.append(GtkLabel)
		self.strLabels.append(label)
		image = Gtk.Image()
		#image.set_from_stock(Gtk.STOCK_CLOSE, Gtk.ICON_SIZE_MENU)
		close = Gtk.Button()
		#close.set_image(image)
		#close.set_relief(Gtk.RELIEF_NONE)
		close.set_focus_on_click(False)
		#print close.get_relief()
		tab.pack_start(self.labels[-1], True, True, 0)
		tab.pack_start(close, False, False, 0)
		tab.show_all()
		sw = Gtk.ScrolledWindow()
		sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)	
		hbox = Gtk.HBox()
		doc = textview.Document(self.handler, self.handler.get_option('textview_bg'), self.handler.get_option('textview_font_color'), text)
		self.docs.append(doc)
		lineNumbers = lines.LineNumbers(self.handler, doc, self.handler.get_option('lines_bg'), self.handler.get_option('lines_font_color'))
		self.lineNumbers.append(lineNumbers)
		hbox.pack_start(self.lineNumbers[-1], False, False, 0)
		hbox.pack_start(self.docs[-1], True, True, 0)
		hbox.show_all()
		sw.add_with_viewport(hbox)
		self.append_page(sw, tab)
		self.set_tab_reorderable(sw, True)
		if self.handler.get_option('show_line_numbers') == 'False':
			for ln in self.lineNumbers:
				ln.hide_all()		
		self.show_all()
		self.set_current_page(-1)
		doc.grab_focus()
		self.files.append(filename)
		close.connect('clicked', self.on_click_close, sw, doc, lineNumbers, filename)
		self.handler.toolbar.activate_actions(None)
	
	def set_tab_dirty(self):
		tab = self.get_current_page()
		label = self.labels[tab].get_text()
		if label[0] == '*':
			pass
		else:
			self.labels[tab].set_text('* '+label)
		
	def set_tab_clean(self):
		tab = self.get_current_page()
		label = self.labels[tab].get_text()
		label = label[1:]
		self.labels[tab].set_text(label)
		
		
	def on_click_close(self, widget, sw, doc, lineNumbers, filePath):
		self.close_tab(sw, doc, lineNumbers, filePath)
		
	def close_tab_by_id(self, tab):
		doc = self.docs[tab]
		lineNumbers = self.lineNumbers[tab]
		if doc.has_unsaved_changes() == False:
			self.remove_page(tab)
			#self.docs.remove(doc)
			#self.lineNumbers.remove(lineNumbers)
		else:
			d = self.handler.prompt_save_dialog()
			response = d.run()
			if response == -1:
				self.remove_page(tab)
			#	self.docs.remove(doc)
			#	self.lineNumbers.remove(lineNumbers)
			elif response == 0:
				pass
			elif response == 1:
				self.handler.save_doc(doc)
				self.remove_page(tab)
			#	self.docs.remove(doc)
			#	self.lineNumbers.remove(lineNumbers)
			d.destroy()
	
	def close_tab(self, sw, doc, lineNumbers, filePath):
		tab = self.page_num(sw)
		#self.set_current_page(tab)
		#if doc.has_unsaved_changes() == False:
		if doc.buffer.get_modified() == False:
			self.remove_page(tab)
			self.docs.remove(doc)
			self.lineNumbers.remove(lineNumbers)
		else:
			d = self.handler.prompt_save_dialog()
			response = d.run()
			if response == -1:
				self.remove_page(tab)
				self.docs.remove(doc)
				self.lineNumbers.remove(lineNumbers)
			elif response == 0:
				pass
			elif response == 1:
				self.handler.save_doc(tab)
				self.remove_page(tab)
				self.docs.remove(doc)
				self.lineNumbers.remove(lineNumbers)
			d.destroy()
			
