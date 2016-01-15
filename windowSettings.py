#!/usr/bin/env python
#encoding: utf8

import gtk, os
import webkit


class windowSettings: 
    def __init__(self, SetCat):
    	self.window = gtk.Window()
        self.window.set_title("Settings")
        #self.window.set_size_request(160, 200)
        color = gtk.gdk.color_parse("#333333")
        self.window.modify_bg(gtk.STATE_NORMAL, color)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_border_width(20)
        #self.window.connect("destroy", gtk.main_quit)
        vbox2 = gtk.VBox(True, 2)
        self.window.add(vbox2)
        label = gtk.Label("<b>Select items to show recommendation</b>")
        label.set_use_markup(True)
        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
        vbox2.pack_start(label, True, True, 0)

        button = gtk.CheckButton("Variables")
        if ("Variables" in SetCat):
            button.set_active(True)
        button.get_child().modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
        button.get_child().modify_fg(gtk.STATE_ACTIVE, gtk.gdk.color_parse('#FFFFFF'))
        button.connect("toggled", self.callback, ["Variables",SetCat])
        vbox2.pack_start(button, True, True, 2)
        button.show()

        button = gtk.CheckButton("Conversion")
        if ("Conversion" in SetCat):
            button.set_active(True)
        button.get_child().modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
        button.get_child().modify_fg(gtk.STATE_ACTIVE, gtk.gdk.color_parse('#FFFFFF'))
        button.connect("toggled", self.callback, ["Conversion", SetCat])
        vbox2.pack_start(button, True, True, 2)
        button.show()

        button = gtk.CheckButton("Return")
        if ("Return" in SetCat):
            button.set_active(True)
        button.get_child().modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
        button.get_child().modify_fg(gtk.STATE_ACTIVE, gtk.gdk.color_parse('#FFFFFF'))
        button.connect("toggled", self.callback, ["Return", SetCat])
        vbox2.pack_start(button, True, True, 2)
        button.show()
        

        button = gtk.CheckButton("Operators")
        if ("Operators" in SetCat):
            button.set_active(True)
        button.get_child().modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
        button.get_child().modify_fg(gtk.STATE_ACTIVE, gtk.gdk.color_parse('#FFFFFF'))
        button.connect("toggled", self.callback, ["Operators",  SetCat])
        vbox2.pack_start(button, True, True, 2)
        button.show()


        button = gtk.CheckButton("Sentences")
        if ("Sentences" in SetCat):
            button.set_active(True)
        button.get_child().modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
        button.get_child().modify_fg(gtk.STATE_ACTIVE, gtk.gdk.color_parse('#FFFFFF'))
        button.connect("toggled", self.callback, ["Sentences",  SetCat])
        vbox2.pack_start(button, True, True, 2)
        button.show()


        button = gtk.CheckButton("Data Types")
        if ("Data Types" in SetCat):
            button.set_active(True)
        button.get_child().modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
        button.get_child().modify_fg(gtk.STATE_ACTIVE, gtk.gdk.color_parse('#FFFFFF'))
        button.connect("toggled", self.callback, ["Data Types",  SetCat])
        vbox2.pack_start(button, True, True, 2)
        button.show()

        buttonOK = gtk.Button("OK")
        buttonOK.connect("clicked", self.on_clicked)
        vbox2.pack_start(buttonOK, True, True, 2)
        buttonOK.show()


        vbox2.show()
        self.window.show_all()


    def on_clicked(self, widget):
       self.window.destroy()


    def callback(self, widget, data=None):
    	if widget.get_active():
        	data[1].append(data[0])
        else:
        	data[1].remove(data[0])



def Sett(SetCat):
	windowSettings(SetCat)
	gtk.main()


