#!/usr/bin/env python
#encoding: utf8

import gtk, os
import webkit

class windowHelp: 
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_title("Recomendaciones")
        self.window.set_size_request(500, 400)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect("destroy", gtk.main_quit)        
        
        #Contenedor de MenuBar y Seccion de feeds   
        self.extContainer = gtk.VBox()
        
       
        #Seccion de indice
        self.container = gtk.HPaned()
        self.container.set_position(150)
                
        #Columna izquierda
        scrolled = gtk.ScrolledWindow()
        scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.selecTree = gtk.TreeView()
        self.selecTree.connect("row-activated", self.showRecommendation)
        
        self.selecCol = gtk.TreeViewColumn("Indice")
        self.selecCol.set_alignment(0.1)
        self.selecCol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        
        cell = gtk.CellRendererText()

        self.selecCol.pack_start(cell, False)
        self.selecCol.add_attribute(cell, "text", 0)

        self.selecTree.append_column(self.selecCol) 
        
        self.selecTreeStore = gtk.TreeStore(str)
        self.selecTree.set_model(self.selecTreeStore)
        structure = self.selecTreeStore.append(None,["Control Structure"]) 
        self.selecTreeStore.append(structure, ["Identation"])
        self.selecTreeStore.append(structure, ["Braces-{}"]) 
        self.selecTreeStore.append(structure, ["Instruction Lines"]) 
        self.selecTreeStore.append(structure, ["Spaces"])
        self.selecTreeStore.append(structure, ["Parenthesis-()"])
        self.selecTreeStore.append(structure, ["Unreachable Instruction"])
        self.selecTreeStore.append(structure, ["Operators ++ and --"])
        self.selecTreeStore.append(structure, ["Loop For"]) 
        self.selecTreeStore.append(structure, ["Sentence Break"])
        self.selecTreeStore.append(structure, ["Sentence Switch"]) 
        variables = self.selecTreeStore.append(None,["Variables"])
        self.selecTreeStore.append(variables, ["Global Variables"])
        self.selecTreeStore.append(variables, ["Variable Names"])
        self.selecTreeStore.append(variables, ["Constant Values"])
        self.selecTreeStore.append(variables, ["Declaration and Inicialization"])
        self.selecTreeStore.append(variables, ["Conversion"])
        comments = self.selecTreeStore.append(None,["Comments"])
        self.selecTreeStore.append(comments, ["Headers"])
        self.selecTreeStore.append(comments, ["Line"])
        self.selecTreeStore.append(comments, ["Block"])
        self.selecTreeStore.append(comments, ["Structure"])



        scrolled.add(self.selecTree)      
        self.container.add1(scrolled)
               
        # Columna derecha
        self.view = webkit.WebView()
        scrolled = gtk.ScrolledWindow()
        scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled.add(self.view)
        self.feedsTree = gtk.TreeView()
        self.feedsTree.set_rules_hint(True)
        
        self.feedsCol = gtk.TreeViewColumn("")
        self.feedsCol.set_alignment(0.5)
        self.feedsCol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
 
        cell = gtk.CellRendererText()
        self.feedsCol.pack_start(cell, False)
        self.feedsCol.add_attribute(cell, "text", 0)
        self.feedsTree.append_column(self.feedsCol)
        
        self.feedsStore = gtk.ListStore(str)            
        self.feedsTree.set_model(self.feedsStore)   
        scrolled.add(self.feedsTree)  
        self.container.add2(scrolled)
        
        self.extContainer.pack_start(self.container)
        	
        self.window.add(self.extContainer)
        
        self.window.show_all()
    
    def showRecommendation(self, treeview, path, column):
        model = treeview.get_model()
        it = model.get_iter(path)
        name_treeview = model.get_value(it, 0)
        print name_treeview
        path = os.path.dirname(os.path.dirname(__file__)) + "/Code_Coach/Repositorio/"

        if name_treeview == "Identation":
            path = path + "identation.html"
            self.view.open(path)
        if name_treeview == "Braces-{}":
            path = path + "prueba.html"
            self.view.open(path)
        else:
            path = path + "error.html"
            self.view.open(path)   

        
        

        
def showWinHelp():
	windowHelp()
	gtk.main()
