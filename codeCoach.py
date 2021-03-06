#!/usr/bin/env python
#encoding: utf8
import windowHelp as wh
import windowSettings as ws
import gtk, pango, os, commands, re

KEYWORDS = ("auto","break","case","char","const","continue","default","do",
    "double","else","enum","extern","float","for","goto","if",
    "int","long","register","return","short","signed","sizeof","static",
    "struct","switch","typedef","union","unsigned","void","volatile","while")

OPERATORS = ("=","+","-","*","/","%","&","|","!",">","<","^","~","?",":")

NUMS = ("0","1","2","3","4","5","6","7","8","9",".")

ESCAPE_CHARS = ("\\t","\\n","%d","%f","%s")

STRINGS = ("\"", "'")

COMMENTS = ("//", "/*")

SetCat= ["Conversion", "Variables", "Return", "Data Types", "Sentences", "Operators"]

Variables= {"return":["Return","Return"],"identifier":["Declaration and Inicialization", "Variables"],"Assignment": ["Conversion", "Conversion"],"Variable": ["Declaration and Inicialization", "Variables"], "out-of-bounds":["Declaration and Inicialization", "Variables"] }

class FileChooserDialog:
    filename=""
    def __init__(self):
        filechooserdialog = gtk.FileChooserDialog("Open File", None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))
        filter1 = gtk.FileFilter()
        filter1.set_name("All")
        filter1.add_pattern("*")
        filechooserdialog.add_filter(filter1)

        filter2 = gtk.FileFilter()
        filter2.set_name("c")
        filter2.add_pattern("*.c")
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
        self.window.set_size_request(900, 600)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect("destroy", lambda w: gtk.main_quit())
        self.rutas = []

        self.extContainer = gtk.VBox()

        toolbar = gtk.Toolbar()
        toolbar.set_style(gtk.TOOLBAR_BOTH)
        
        btnNew = gtk.ToolButton(gtk.STOCK_NEW)
        btnNew.set_label("New")
        separator1 = gtk.SeparatorToolItem()
        btnOpen = gtk.ToolButton(gtk.STOCK_OPEN)
        btnOpen.set_label("Open")
        separator2 = gtk.SeparatorToolItem()
        btnSave = gtk.ToolButton(gtk.STOCK_SAVE)
        btnSave.set_label("Save")
        separator3 = gtk.SeparatorToolItem()
        btnPref = gtk.ToolButton(gtk.STOCK_HELP)
        btnPref.set_label("Help")    
        separator4 = gtk.SeparatorToolItem()
        btnSett = gtk.ToolButton(gtk.STOCK_PREFERENCES)
        btnSett.set_label("Settings")        
        
        
        btnNew.connect("clicked", self.newDoc)
        btnOpen.connect("clicked", self.openwindow)
        btnSave.connect("clicked", self.savewindow)
        btnPref.connect("clicked", self.openHelp)
        btnSett.connect("clicked", self.showSettings)
        toolbar.insert(btnNew, 0)
        toolbar.insert(separator1, 1)
        toolbar.insert(btnOpen, 2)
        toolbar.insert(separator2, 3)
        toolbar.insert(btnSave, 4)
        toolbar.insert(separator3,5)
        toolbar.insert(btnPref,6)
        toolbar.insert(separator4,7)
        toolbar.insert(btnSett,8)

        self.extContainer.pack_start(toolbar, expand=False)


        self.notebook = gtk.Notebook()
        self.notebook.set_scrollable(True)
        self.newDoc(None)
        self.notebook.connect("switch-page", self.changeTitle)

        eb = gtk.EventBox()
        eb.add(self.notebook)
        eb.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#333333"))
        self.extContainer.pack_start(eb)
        
        self.notifyScroll = gtk.ScrolledWindow()
        self.notifyScroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        self.extContainer.pack_start(self.notifyScroll)

        self.window.add(self.extContainer)
        self.window.show_all()


    def changeTitle(self, notebook, page, page_num):
        self.window.set_title(self.rutas[page_num])


    def on_text_view_expose_event(self, text_view, event):
        text_buffer = text_view.get_buffer()
        bounds = text_buffer.get_bounds()
        text = text_buffer.get_text(*bounds)
        nlines = text.count("\n") + 1
        layout = pango.Layout(text_view.get_pango_context())
        layout.set_markup("\n".join([str(x + 1) for x in range(nlines)]))
        layout.set_alignment(pango.ALIGN_LEFT)
        width = layout.get_pixel_size()[0]
        text_view.set_border_window_size(gtk.TEXT_WINDOW_LEFT, width + 4)
        y = -text_view.window_to_buffer_coords(gtk.TEXT_WINDOW_LEFT, 2, 0)[1]
        window = text_view.get_window(gtk.TEXT_WINDOW_LEFT)
        window.clear()
        text_view.style.paint_layout(window=window,
                                     state_type=gtk.STATE_NORMAL,
                                     use_text=False,
                                     area=None,
                                     widget=text_view,
                                     detail=None,
                                     x=2,
                                     y=y,
                                     layout=layout)


    def on_closetab_button_clicked(self, sender, widget):
        pagenum = self.notebook.page_num(widget)     
        self.notebook.remove_page(pagenum)
        self.rutas.pop(pagenum)
  

    def newDoc(self, widget=None):
        self.create_page()

        
    def create_page(self, title="Untitled", ruta="", filetext=""):
        tab = gtk.HBox(False, 0)
        tab_label = gtk.Label(title)
        tab.pack_start( tab_label )

        #make the close button
        btn = gtk.Button()
        btn.set_relief(gtk.RELIEF_NONE)
        btn.set_focus_on_click(False)
        close_image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        btn.add(close_image)
        tab.pack_start(btn, False, False)
        tab.show_all()

        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        textArea = gtk.TextView()
        textArea.set_border_window_size(gtk.TEXT_WINDOW_LEFT, 24)
        textArea.modify_font(pango.FontDescription("Courier New bold 10"))
        textArea.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#333333"))
        textArea.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))

        tabs = pango.TabArray(1, True)
        tabs.set_tab(0, pango.TAB_LEFT, 33)
        textArea.set_tabs(tabs)

        textArea.connect("expose-event", self.on_text_view_expose_event)

        textbuffer = textArea.get_buffer()
        textbuffer.set_text(filetext)
        textbuffer.create_tag("keyword", foreground="cyan")
        textbuffer.create_tag("operator", foreground="#ff0066")
        textbuffer.create_tag("num", foreground="#9966cc")       
        textbuffer.create_tag("string", foreground="#ffff66")
        textbuffer.create_tag("escape_char", foreground="#9966cc")
        textbuffer.create_tag("comment", foreground="gray")

        if title[-2:] == ".c":
            self.verify_keychars(textbuffer)
            textbuffer.connect("changed", self.verify_keychars)
        
        sw.add(textArea)

        btn.connect('clicked', self.on_closetab_button_clicked, sw)             
        
        self.notebook.append_page(sw, tab)
        
        self.window.show_all()
        self.rutas.append(ruta + "Code Coach")
        self.notebook.set_page(-1)


    def verify_keychars(self, textbuffer):
        textbuffer.remove_tag_by_name("keyword", textbuffer.get_start_iter(), textbuffer.get_end_iter())
        textbuffer.remove_tag_by_name("operator", textbuffer.get_start_iter(), textbuffer.get_end_iter())
        textbuffer.remove_tag_by_name("num", textbuffer.get_start_iter(), textbuffer.get_end_iter())
        textbuffer.remove_tag_by_name("string", textbuffer.get_start_iter(), textbuffer.get_end_iter())
        textbuffer.remove_tag_by_name("escape_char", textbuffer.get_start_iter(), textbuffer.get_end_iter())
        textbuffer.remove_tag_by_name("comment", textbuffer.get_start_iter(), textbuffer.get_end_iter())
        for keyword in KEYWORDS:
            self.search(textbuffer, keyword, textbuffer.get_start_iter(), "keyword")
        for oper in OPERATORS:
            self.search(textbuffer, oper, textbuffer.get_start_iter(), "operator")
        for num in NUMS:
            self.search(textbuffer, num, textbuffer.get_start_iter(), "num")
        for string in STRINGS:
            self.search(textbuffer, string, textbuffer.get_start_iter(), "string")
        for ec in ESCAPE_CHARS:
            self.search(textbuffer, ec, textbuffer.get_start_iter(), "escape_char")       
        for comment in COMMENTS:
            self.search(textbuffer, comment, textbuffer.get_start_iter(), "comment")
         

    def search(self, textbuffer, text, start, tag_name):
        end = textbuffer.get_end_iter()
        match = start.forward_search(text, 0, end)

        if match != None:
            match_start, match_end = match

            if tag_name == "keyword":
                if match_start.starts_word() and match_end.ends_word():
                    textbuffer.apply_tag_by_name(tag_name, match_start, match_end)

            elif tag_name == "string":
                nextComilla = match_end.forward_search(text, 0)
                if nextComilla != None:
                    start_nextComilla, match_end = nextComilla
                    textbuffer.apply_tag_by_name(tag_name, match_start, match_end)

            elif tag_name == "comment":
                if text == "//":
                    line_end = match_end.forward_search("\n", 0)
                    if line_end != None:
                        start_line_end, match_end = line_end
                        textbuffer.apply_tag_by_name(tag_name, match_start, match_end)
                else:
                    comment_end = match_end.forward_search("*/", 0)
                    if comment_end != None:
                        start_comment_end, match_end = comment_end
                        textbuffer.apply_tag_by_name(tag_name, match_start, match_end)

            else:
                textbuffer.apply_tag_by_name(tag_name, match_start, match_end)

            self.search(textbuffer, text, match_end, tag_name)


    def openwindow(self,widget):
        a=FileChooserDialog()
        print a.filename
        f = open(a.filename, 'r')
        code= f.read()
        f.close()

        if "\\" in a.filename:
            flname = a.filename.split("\\")[-1]
        else:
            flname = a.filename.split("/")[-1]
        
        self.create_page(flname, a.filename+" - ", code)

    def openHelp(self, widget):
        item=""
        wh.showWinHelp(item)




    def showSettings(self, widget):
        ws.Sett(SetCat)








    def savewindow(self,widget):       
        text_filter=gtk.FileFilter()
        text_filter.set_name("Text file")
        text_filter.add_mime_type("text/*")
        all_filter=gtk.FileFilter()
        all_filter.set_name("All")
        all_filter.add_pattern("*")
        filename=None

        pageNum = self.notebook.get_current_page()
        pageCurrent = self.notebook.get_nth_page(pageNum)
        textviewCurrent=pageCurrent.get_child()
        textbuffer=textviewCurrent.get_buffer()
        start_iter = textbuffer.get_start_iter()
        end_iter = textbuffer.get_end_iter()
        newcode= textbuffer.get_text(start_iter, end_iter, True)

        title = self.rutas[pageNum]
        filename = title[:-13] #para eliminar ( - CodeCoach)
        #print os.path.exists(filename)
        if "\\" in filename:
            docName = filename.split("\\")[-1]
        else:
            docName = filename.split("/")[-1]

        
        if os.path.exists(filename) == True:
            
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
            print  "Cambios guardados"
   
        else:

            dialog=gtk.FileChooserDialog(title="Guardar archivo", action=gtk.FILE_CHOOSER_ACTION_SAVE,
                buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
            
            if (text_filter != None) and (all_filter != None):
                dialog.add_filter(text_filter)
                dialog.add_filter(all_filter)
                
            response = dialog.run()

            if response == gtk.RESPONSE_CANCEL:
                dialog.destroy()
                    
            if response == gtk.RESPONSE_OK:

                filename = dialog.get_filename()
                self.rutas[pageNum] = filename + " - Code Coach"
                
                if "\\" in filename:
                    docName = filename.split("\\")[-1]
                else:
                    docName = filename.split("/")[-1]

                if docName[-2:] == ".c":
                    self.verify_keychars(textbuffer)
                    textbuffer.connect("changed", self.verify_keychars)

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

        self.analize_code(filename)

    def analize_code(self, file_path):

        output = commands.getoutput("splint "+file_path+" +bounds -hints")
        split = output.split("\n")
        output = "\n".join(split[2:])
        if "(For help" in output:
            regex = re.search(r"\(\bFor help\b.*\)", output, re.DOTALL).group(0)
            output = output.replace(regex,"")

        if "\\" in file_path:
            flname = file_path.split("\\")[-1]
        else:
            flname = file_path.split("/")[-1]
        outp = output.split("\n")
        boxP= self.notifyScroll.get_child()
        if(boxP!= None):
            self.notifyScroll.remove(boxP)
        boxP=self.AddNotify(outp,flname)
        self.notifyScroll.add_with_viewport(boxP)
        self.notifyScroll.show_all()



    def AddNotify(self, outp, flname):
        box1 = gtk.VBox(spacing=6)
        for i in outp:
            if i!= outp[0]:
                i=i.replace("../../"+flname+":","Line ")
            else:
                i=i.replace("../../","")
            box2 = gtk.HBox(spacing=0)
            line = gtk.Label()
            line.set_text(i)
            line.set_alignment(0, 0)
            event_box = gtk.EventBox()
            event_box.show()
            box2.pack_start(line, True, True, 50)
            if self.makeLink(i, outp,flname):
                label = gtk.Label("Check Recommendation")
                label.set_markup("<span foreground=\"blue\" underline=\"single\">" +
                label.get_text() + "</span>")
                label.show()
                event_box.add(label)
                event_box.set_events(gtk.gdk.BUTTON_PRESS_MASK)
                event_box.show()
                event_box.connect("button_press_event", self.callback2,i)
                box2.pack_start(event_box, False, True, 80)
            box1.pack_start(box2, False, False, 3)
        return box1
            
        
          
        
        
    def callback2(self, widget,event,data=None):
        
        item="Identation"
        for elem in Variables:
            if str(elem).upper() in data.upper():
                item=Variables[elem][0]

        wh.showWinHelp(item)
    




    
    def makeLink(self, line, outp,flname):
        cm=True
        if line == outp[0] or ("@ Line" in line) or "Line" not in line or line == "" or line == outp[-1]:
            cm=False
        for elem in Variables:
            if str(elem).upper() in line.upper():
                item=Variables[elem][1]
                if item not in SetCat:
                    cm= False
        

        return cm

        


           
        
         

MainWindow()
gtk.main()
