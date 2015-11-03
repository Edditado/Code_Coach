#!/usr/bin/env python
#encoding: utf8

import gtk
import os

class FileChooserDialog:
    filename=""
    def __init__(self):
        filechooserdialog = gtk.FileChooserDialog("Abrir archivo", None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))
        filter1 = gtk.FileFilter()
        filter1.set_name("Todos")
        filter1.add_pattern("*")
        filechooserdialog.add_filter(filter1)

        filter2 = gtk.FileFilter()
        filter2.set_name("python")
        filter2.add_pattern("*.py")
        filechooserdialog.add_filter(filter2)
        response = filechooserdialog.run()
        
        
        if response == gtk.RESPONSE_OK:
            self.filename = filechooserdialog.get_filename()
            
        filechooserdialog.destroy()


        
class confirmOverwriteFileDialog:
    cansave = False
    def __init__(self,filename, parent):
        dialog = gtk.Dialog(( 'Confirmar' ), parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, ( gtk.STOCK_YES, gtk.RESPONSE_ACCEPT, gtk.STOCK_NO, gtk.RESPONSE_REJECT ) )
        dialog.vbox.pack_start( gtk.Label(( 'El archivo "%s" ya existe' ) % ( filename, ) ) )
        dialog.vbox.pack_start( gtk.Label(( 'Desea reemplazarlo?' ) ) )
        
        dialog.show_all()
        response = dialog.run()
        if response == gtk.RESPONSE_ACCEPT:
            self.cansave = True
            dialog.destroy()
        else:
            dialog.destroy()
        



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
        btnOpen.connect("clicked", self.openwindow)
        btnSave.connect("clicked", self.savewindow)
        toolbar.insert(btnNew, 0)
        toolbar.insert(separator1, 1)
        toolbar.insert(btnOpen, 2)
        toolbar.insert(separator2, 3)
        toolbar.insert(btnSave, 4)

        extContainer.pack_start(toolbar, expand=False)


        self.notebook = gtk.Notebook()
        self.notebook.set_scrollable(True)
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        textArea = gtk.TextView()
        sw.add(textArea)

        tab = gtk.HBox(False, 0)
        tab_label = gtk.Label("Untitled")
        tab.pack_start( tab_label )

        #get a stock close button image
        close_image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        
        
        #make the close button
        btn = gtk.Button()
        btn.set_relief(gtk.RELIEF_NONE)
        btn.set_focus_on_click(False)
        btn.add(close_image)
        tab.pack_start(btn, False, False)
        tab.show_all()
        
        self.notebook.append_page(sw, tab)

        btn.connect('clicked', self.on_closetab_button_clicked, sw)

        extContainer.pack_start(self.notebook)
        
        align = gtk.Alignment(xalign=0.01)
        notify = gtk.Label("\n")
        notify.set_justify(gtk.JUSTIFY_LEFT)
        align.add(notify)

        extContainer.pack_start(align, expand=False)

        

        self.window.add(extContainer)
        self.window.show_all()

    def on_closetab_button_clicked(self, sender, widget):
        #get the page number of the tab we wanted to close
        pagenum = self.notebook.page_num(widget)
       
        #and close it
        self.notebook.remove_page(pagenum)
            
    def newDoc(self, widget):
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        newTextArea = gtk.TextView()
        sw.add(newTextArea)
                     

        tab = gtk.HBox(False, 0)
        tab_label = gtk.Label("Untitled")
        tab.pack_start( tab_label )

        #get a stock close button image
        close_image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        
        #make the close button
        btn = gtk.Button()
        btn.set_relief(gtk.RELIEF_NONE)
        btn.set_focus_on_click(False)
        btn.add(close_image)
        tab.pack_start(btn, False, False)
        tab.show_all()
        
        self.notebook.append_page(sw, tab)
        btn.connect('clicked', self.on_closetab_button_clicked, sw)

        #self.notebook.set_focus_child(sw)
        self.window.show_all()
        #self.notebook.set_page(-1)

    def openwindow(self,widget):
        a=FileChooserDialog()
        f = open(a.filename, 'r')
        code= f.read()
        f.close()
        print a.filename
        if "\\" in a.filename:
            flname = a.filename.split("\\")[-1]
        else:
            flname = a.filename.split("/")[-1]
        
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        textbuffer = gtk.TextBuffer()
        textbuffer.set_text(code)
        textAreaCode = gtk.TextView()
        textAreaCode.set_buffer(textbuffer)
        sw.add(textAreaCode)

        tab = gtk.HBox(False, 0)
        tab_label = gtk.Label(flname)
        tab.pack_start( tab_label )

        #get a stock close button image
        close_image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        
        #make the close button
        btn = gtk.Button()
        btn.set_relief(gtk.RELIEF_NONE)
        btn.set_focus_on_click(False)
        btn.add(close_image)
        tab.pack_start(btn, False, False)
        tab.show_all()


        self.notebook.append_page(sw, tab)

        btn.connect('clicked', self.on_closetab_button_clicked, sw)
        #self.notebook.set_focus_child(sw)
        self.window.set_title(a.filename + " - Code Coach")
        self.window.show_all()
        #self.notebook.set_page(-1)


    def savewindow(self,widget):
        
        text_filter=gtk.FileFilter()
        text_filter.set_name("Archivos de texto")
        text_filter.add_mime_type("text/*")
        all_filter=gtk.FileFilter()
        all_filter.set_name("Todos")
        all_filter.add_pattern("*")
        filename=None
        dialog=gtk.FileChooserDialog(title="Guardar archivo", action=gtk.FILE_CHOOSER_ACTION_SAVE,
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
          
        if (text_filter != None) and (all_filter != None):
            dialog.add_filter(text_filter)
            dialog.add_filter(all_filter)
            
        response = dialog.run()
        if response == gtk.RESPONSE_CANCEL:
            dialog.destroy()
                
        if response == gtk.RESPONSE_OK:

            cansave= False

            filename = dialog.get_filename()
            if "\\" in filename:
                docName = filename.split("\\")[-1]
            else:
                docName = filename.split("/")[-1]    

            pageNum = self.notebook.get_current_page()
            pageCurrent = self.notebook.get_nth_page(pageNum)
            textviewCurrent=pageCurrent.get_child()
            textbuffer=textviewCurrent.get_buffer()
            start_iter = textbuffer.get_start_iter()
            end_iter = textbuffer.get_end_iter()
            newcode= textbuffer.get_text(start_iter, end_iter, True)
            

            if os.path.exists(dialog.get_filename()) == True:
               
                dialog2=confirmOverwriteFileDialog(filename, dialog)

                if dialog2.cansave == True:
                    cansave = True
                    if filename != None:
                        fileNew=open(filename, 'w')
                        fileNew.write(newcode)
                        fileNew.close()

                        tab = gtk.HBox(False, 0)
                        tab_label = gtk.Label(docName)
                       
                        tab.pack_start( tab_label )

                        #get a stock close button image
                        close_image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
                        
                        #make the close button
                        btn = gtk.Button()
                        btn.set_relief(gtk.RELIEF_NONE)
                        btn.set_focus_on_click(False)
                        btn.add(close_image)
                        tab.pack_start(btn, False, False)
                        tab.show_all()
                        
                        self.notebook.set_tab_label(pageCurrent,tab)
                        btn.connect('clicked', self.on_closetab_button_clicked, pageCurrent)

                        self.window.set_title(filename + " - Code Coach")
                        self.window.show_all()
                    dialog.destroy()
                else:
                    dialog.destroy()
                    
            else:
                cansave = True
                if cansave == True: 
                    if filename != None:
                        fileNew=open(filename, 'w')
                        fileNew.write(newcode)
                        fileNew.close()

                        tab = gtk.HBox(False, 0)
                        tab_label = gtk.Label(docName)
                       
                        tab.pack_start( tab_label )

                        #get a stock close button image
                        close_image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
                        
                        #make the close button
                        btn = gtk.Button()
                        btn.set_relief(gtk.RELIEF_NONE)
                        btn.set_focus_on_click(False)
                        btn.add(close_image)
                        tab.pack_start(btn, False, False)
                        tab.show_all()
                        
                        self.notebook.set_tab_label(pageCurrent,tab)
                        btn.connect('clicked', self.on_closetab_button_clicked, pageCurrent)

                        self.window.set_title(filename + " - Code Coach")
                        self.window.show_all()
                    dialog.destroy()
                else:
                    pass

    


           
        
  



    
            

MainWindow()
gtk.main()
