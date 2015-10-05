#!/usr/bin/env python
#encoding: utf8

import gtk


class MainWindow: 
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_title("Code Coach")
        self.window.set_size_request(800, 500)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect("destroy", lambda w: gtk.main_quit())

        extContainer = gtk.VBox()

        toolbar = gtk.Toolbar()
        toolbar.set_style(gtk.TOOLBAR_BOTH)
        
        btnNew = gtk.ToolButton(gtk.STOCK_NEW)
        separator1 = gtk.SeparatorToolItem()
        btnOpen = gtk.ToolButton(gtk.STOCK_OPEN)
        separator2 = gtk.SeparatorToolItem()
        btnSave = gtk.ToolButton(gtk.STOCK_SAVE)
        
        btnNew.connect("clicked", self.newDoc)

        toolbar.insert(btnNew, 0)
        toolbar.insert(separator1, 1)
        toolbar.insert(btnOpen, 2)
        toolbar.insert(separator2, 3)
        toolbar.insert(btnSave, 4)

        extContainer.pack_start(toolbar, expand=False)

        self.notebook = gtk.Notebook()
        textArea = gtk.TextView()
        self.notebook.append_page(textArea, gtk.Label("Empty document"))

        extContainer.pack_start(self.notebook)
        
        align = gtk.Alignment(xalign=0.01)
        notify = gtk.Label("\n")
        notify.set_justify(gtk.JUSTIFY_LEFT)
        align.add(notify)

        extContainer.pack_start(align, expand=False)

        self.window.add(extContainer)
        self.window.show_all()


    def newDoc(self, widget):
        newTextArea = gtk.TextView()
        nPages = self.notebook.get_n_pages()
        numDoc = 0
        for i in xrange(nPages):
            pag = self.notebook.get_nth_page(i)
            labelName = self.notebook.get_tab_label_text(pag).split("(")
            if labelName[0] == "Empty document":
                numDoc += 1
        if numDoc == 0:
            self.notebook.append_page(newTextArea, gtk.Label("Empty document"))
        else: 
            self.notebook.append_page(newTextArea, gtk.Label("Empty document("+str(numDoc)+")"))

        self.window.show_all()


MainWindow()
gtk.main()
