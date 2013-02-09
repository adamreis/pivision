import gtk

class PyApp(gtk.Window):
    def __init__(self):
        super(PyApp, self).__init__()
        
        self.set_title("alignment")
        self.set_size_request(600,400)
        self.set_position(gtk.WIN_POS_CENTER)
        

        vbox = gtk.VBox(False,2)

        mb = gtk.MenuBar()
        filemenu = gtk.Menu()
        filem = gtk.MenuItem("file") 
        filem.set_submenu(filemenu)
        mb.append(filem)

        vbox.pack_start(mb, False, False, 0)

        table = gtk.Table(5,4, True)
        
        table.attach(gtk.Button("fart"),0,1,0,1)
        table.attach(gtk.Button("poop"),1,2,0,1)

        vbox.pack_start(gtk.Entry(), False, False, 0)
        vbox.pack_end(table,True,True,0)

        self.add(vbox)

        self.set_tooltip_text("window widget")
        self.connect("destroy", gtk.main_quit)

        self.show_all()
PyApp()
gtk.main()
