import gtk
import sys
import os
import mutagen
import locale
import urllib

TARGET_TYPE_URI_LIST = 80
dnd_list = [ ( 'text/uri-list', 0, TARGET_TYPE_URI_LIST ) ]

class Player():
    def on_dither_dialog_destroy(self, widget, data=None):
        gtk.main_quit()

    def on_filechooserbutton1_file_set(self, widget, data=None):
        self.text_buffer.set_text("")
        get_metadata(widget.get_filename(), self)

    def on_textview1_drag_data_received(self, widget, context, x, y, selection, target_type, timestamp):
        uri = selection.data.strip('\r\n\x00')
        uri_splitted = uri.split() # we may have more than one file dropped
        try:
            len(uri_splitted[1])
            self.text_buffer.set_text("One file at a time, junior.")
        except:
            path = get_file_path_from_dnd_dropped_uri(uri_splitted[0])
            get_metadata(path, self)

    def motion_cb(self, wid, context, x, y, time):
        context.drag_status(gtk.gdk.ACTION_COPY, time)
        return True

    def __init__(self, args):
        builder = gtk.Builder()
        builder.add_from_file("resources/dither.xml")
        self.window = builder.get_object("dither_dialog")
        self.text_buffer = builder.get_object("textbuffer1")
        self.filechooserbutton = builder.get_object("filechooserbutton1")
        self.textview = builder.get_object("textview1")
        self.textview.drag_dest_set( gtk.DEST_DEFAULT_MOTION |
           gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP,
           dnd_list, gtk.gdk.ACTION_COPY)
        builder.connect_signals(self)

class Dither():
    def run(self, filename):
        player = Player(filename)
        if filename:
            get_metadata(filename, player)
        player.window.show()
        gtk.main()

def get_file_path_from_dnd_dropped_uri(uri):
    # get the path to file
    path = ""
    if uri.startswith('file:\\\\\\'): # windows
        path = uri[8:] # 8 is len('file:///')
    elif uri.startswith('file://'): # nautilus, rox
        path = uri[7:] # 7 is len('file://')
    elif uri.startswith('file:'): # xffm
        path = uri[5:] # 5 is len('file:')
    path = urllib.url2pathname(path) # escape special chars
    path = path.strip('\r\n\x00') # remove \r\n and NULL
    return path

def get_metadata(filename, player):
    player.filechooserbutton.set_filename(filename)
    enc = locale.getpreferredencoding()
    try: 
        metadata = mutagen.File(filename)
        player.text_buffer.set_text(metadata.pprint().encode(enc, 'replace'))
    except AttributeError: player.text_buffer.set_text("That's not a music file!")
    except KeyboardInterrupt: raise
    except TypeError:
        player.text_buffer.set_text("One file at a time, junior.")
    except IOError:
        player.text_buffer.set_text("A folder? Just who do you think you are?")
    except Exception, err: player.text_buffer.set_text(str(err))

def main(filename):
    dither = Dither()
    sys.exit(dither.run(filename))
