#!/usr/bin/env python
#encoding: utf8

import gtk, os
import webkit

catG={"Control Structures": (0,), "Identation": (0,0), "Braces": (0,1), "Instruction Lines": (0,2),
   "Spaces": (0,3) , "Parenthesis": (0,4),  "Operators": (0,6), "Loop For": (0,8),  "Return": (0,9),
    "Global Variables": (1,0), "Variable Names": (1,1), "Constant Values" : (1,2), "Declaration and Inicialization": (1,3),
    "Conversion": (1,4), "Headers": (2,0), "Line": (2,1), "Block": (2,2), "Structure": (2,3)}



class windowHelp: 
    def __init__(self, item):
        self.window = gtk.Window()
        self.window.set_title("Recomendaciones")
        self.window.set_size_request(600, 500)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect("destroy", gtk.main_quit)        
        
        #Contenedor de MenuBar y Seccion de html
        self.extContainer = gtk.VBox()
        
       
        #Seccion de indice
        self.container = gtk.HPaned()
        self.container.set_position(150)
                
        #Columna izquierda
        scrolled = gtk.ScrolledWindow()
        scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        self.selecTree = gtk.TreeView()

        self.selecTree.connect("row-activated", self.showRecommendation)

        #path=self.selecTree.get_path("Identation")
        
        
        self.selecCol = gtk.TreeViewColumn("Indice")
        self.selecCol.set_alignment(0.1)
        self.selecCol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

        

        cell = gtk.CellRendererText()

        self.selecCol.pack_start(cell, False)
        self.selecCol.add_attribute(cell, "text", 0)

        self.selecTree.append_column(self.selecCol) 
        
        self.selecTreeStore = gtk.TreeStore(str)
        self.selecTree.set_model(self.selecTreeStore)
        structure = self.selecTreeStore.append(None,["Control Structures"]) 
        self.selecTreeStore.append(structure, ["Identation"])
        self.selecTreeStore.append(structure, ["Braces-{}"]) 
        self.selecTreeStore.append(structure, ["Instruction Lines"]) 
        self.selecTreeStore.append(structure, ["Spaces"])
        self.selecTreeStore.append(structure, ["Parenthesis-()"])
        self.selecTreeStore.append(structure, ["Unreachable Code"])
        self.selecTreeStore.append(structure, ["Operators"])
        self.selecTreeStore.append(structure, ["Loop For"]) 
        self.selecTreeStore.append(structure, ["Sentences goto, break y continue"])
        self.selecTreeStore.append(structure, ["Return"]) 
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
        if item!="":
            self.selecTree.row_activated(catG[item],self.selecCol)
        
        self.window.show_all()
    
    def showRecommendation(self, treeview, path, column):
        model = treeview.get_model()
        it = model.get_iter(path)
        name_treeview = model.get_value(it, 0)
        path = os.path.dirname(os.path.dirname(__file__)) + "/Code_Coach/Repositorio/"

        if (name_treeview != "Control Structures" and name_treeview != "Variables" and name_treeview != "Comments"):
            if name_treeview == "Identation":
                path = path + "Identation.html"
                self.view.open(path)
            if name_treeview == "Braces-{}":
                path = path + "braces.html"
                self.view.open(path)
            if name_treeview == "Instruction Lines":
                path = path + "instructionlines.html"
                self.view.open(path)
            if name_treeview == "Spaces":
                path = path + "spaces.html"
                self.view.open(path)     
            if name_treeview == "Parenthesis-()":
                path = path + "parenthesis.html"
                self.view.open(path)
            if name_treeview == "Unreachable Code":
                path = path + "unreachable.html"
                self.view.open(path)
            if name_treeview == "Operators":
                path = path + "operators.html"
                self.view.open(path)    
            if name_treeview == "Loop For":
                path = path + "for.html"
                self.view.open(path) 
            if name_treeview == "Sentences goto, break y continue":
                path = path + "break.html"
                self.view.open(path) 
            if name_treeview == "Return":
                path = path + "return.html"
                self.view.open(path)
            if name_treeview == "Global Variables":
                path = path + "global.html"
                self.view.open(path)
            if name_treeview == "Variable Names":
                path = path + "variableNames.html"
                self.view.open(path)
            if name_treeview == "Constant Values":
                path = path + "ConstantValues.html"
                self.view.open(path)
            if name_treeview == "Declaration and Inicialization":
                path = path + "declAndInit.html"
                self.view.open(path)
            if name_treeview == "Conversion":
                path = path + "Conversion.html"
                self.view.open(path)
            if name_treeview == "Headers":
                path = path + "headers.html"
                self.view.open(path)
            if name_treeview == "Line":
                path = path + "line.html"
                self.view.open(path)
            if name_treeview == "Block":
                path = path + "block.html"
                self.view.open(path)    
            if name_treeview == "Structure":
                path = path + "structure.html"
                self.view.open(path)                                                        
        else:
            path = path + "error.html"
            self.view.open(path)
            

        
        

        
def showWinHelp(item):
	windowHelp(item)
	gtk.main()
