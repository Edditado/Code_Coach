#!/usr/bin/env python
#encoding: utf8

import gtk


class MainWindow: 
    def __init__(self):
        window = gtk.Window()
        window.set_title("Code Coach")
        window.set_size_request(800, 500)
        window.set_position(gtk.WIN_POS_CENTER)
        window.connect("destroy", lambda w: gtk.main_quit())

        extContainer = gtk.VBox()

        toolbar = gtk.Toolbar()
        toolbar.set_style(gtk.TOOLBAR_BOTH)
        
        btnNew = gtk.ToolButton(gtk.STOCK_NEW)
        separator1 = gtk.SeparatorToolItem()
        btnOpen = gtk.ToolButton(gtk.STOCK_OPEN)
        separator2 = gtk.SeparatorToolItem()
        btnSave = gtk.ToolButton(gtk.STOCK_SAVE)
        
        toolbar.insert(btnNew, 0)
        toolbar.insert(separator1, 1)
        toolbar.insert(btnOpen, 2)
        toolbar.insert(separator2, 3)
        toolbar.insert(btnSave, 4)

        extContainer.pack_start(toolbar, expand=False)

        notebook = gtk.Notebook()
        label = gtk.Label()
        notebook.append_page(label, gtk.Label("Documento vacío"))
        extContainer.pack_start(notebook)
        
        window.add(extContainer)
        window.show_all()


MainWindow()
gtk.main()

"""#!/usr/bin/env python

import gtk

class Notebook:
    def __init__(self):
        window = gtk.Window()
        window.set_default_size(200, 200)
        
        notebook = gtk.Notebook()
        for page in range(0, 3):
            label = gtk.Label()
            notebook.append_page(label)

        window.connect("destroy", lambda w: gtk.main_quit())
        
        window.add(notebook)
        window.show_all()

Notebook()
gtk.main()"""