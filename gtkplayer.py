import os

import pygtk, gtk, gobject

from callback_dict import CallbackDict

class GTK_Main(CallbackDict):
  def __init__(self):
    super(GTK_Main, self).__init__()
    gtk.gdk.threads_init()
    self.init_ui()

  def run(self):
    gtk.threads_enter()
    gtk.main()
    gtk.threads_leave()
    
  def quit(self):
    gtk.main_quit()

  def set_ui_state(self, state):
    print "ui_state", state
    if state == "STOP":
      self.jump_to = None
      self.play_button.set_label(">")
      self.toggle_controls (True)
      self.pos_slider.set_value (0)
    elif state == "PLAY":
      self.play_button.set_label("||")
      self.toggle_controls (False)
    elif state == "PAUSE":
      self.play_button.set_label(">")
      self.toggle_controls (True)

  def init_ui(self):
    self.last_folder = None

    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window = window
    window.set_title("Playbin Player")
    window.set_default_size(240, 240)
    window.connect("destroy", lambda *args: self.call_callbacks("destroy"))

    vbox = gtk.VBox()
    window.add(vbox)
    self.control_panel = gtk.VBox ()
    self.movie_window = gtk.DrawingArea()
    vbox.add_with_properties(self.control_panel, "expand", False)
    vbox.add_with_properties(self.movie_window, "expand", True)
    vbox = self.control_panel

    hbox = gtk.HBox()
    vbox.add (hbox)
    self.prev_button = gtk.Button("<<")
    self.prev_button.connect("clicked", lambda *args: self.call_callbacks("advance", -1))
    hbox.add_with_properties(self.prev_button, "expand", False)
    self.fname_entry = gtk.Entry(); self.fname_entry.set_property ("editable", False)
    hbox.add(self.fname_entry)
    self.open_button = gtk.Button("Open")
    self.open_button.connect("clicked", self.on_open)
    hbox.add_with_properties(self.open_button, "expand", False)
    self.play_button = gtk.Button(">")
    self.play_button.connect("clicked", lambda *args: self.call_callbacks("playpause"))
    hbox.add_with_properties(self.play_button, "expand", False)
    self.stop_button = gtk.Button("Stop")
    self.stop_button.connect("clicked", lambda *args: self.call_callbacks("stop"))
    hbox.add_with_properties(self.stop_button, "expand", False)

    self.iofn_hbox = gtk.HBox()
    hbox.add_with_properties(self.iofn_hbox, "expand", False)
    self.iofn_spin = gtk.SpinButton (gtk.Adjustment (1, 1, 10000, 1, 5, 0), 0, 0)
    self.iofn_spin.set_wrap (True)
    self.iofn_spin.connect("value-changed", self.on_iofn_changed)
    self.iofn_hbox.add_with_properties(self.iofn_spin, "expand", False)
    self.ofn_label = gtk.Label ()
    self.iofn_hbox.add_with_properties(self.ofn_label)

    self.next_button = gtk.Button(">>")
    self.next_button.connect("clicked", lambda *args: self.call_callbacks("advance", 1))
    hbox.add_with_properties(self.next_button, "expand", False)

    hbox = gtk.HBox()
    vbox.add (hbox)
    self.slow_button = gtk.Button("Slower")
    self.slow_button.connect("clicked", lambda *args: self.call_callbacks("slower"))
    hbox.add_with_properties(self.slow_button)
    self.speed1_button = gtk.Button("1x")
    self.speed1_button.connect("clicked", lambda *args: self.call_callbacks("normal_speed"))
    hbox.add(self.speed1_button)
    self.fast_button = gtk.Button("Faster")
    self.fast_button.connect("clicked", lambda *args: self.call_callbacks("faster"))
    hbox.pack_end(self.fast_button)

    hbox = gtk.HBox()
    vbox.add (hbox)
    self.on_backward_button = gtk.Button ("<-")
    self.on_backward_button.connect("clicked", lambda *args: self.call_callbacks("backward"))
    hbox.add_with_properties(self.on_backward_button, "expand", False)
    self.pos_slider = gtk.HScale (gtk.Adjustment (0.0, 0.0, 101.5, 0.5, 2.0, 1.5))
    self.pos_slider.set_update_policy(gtk.UPDATE_DISCONTINUOUS)
    self.pos_slider.connect("change-value", self.on_change_position1)
    self.pos_slider.connect("value-changed", self.on_change_position2)
    hbox.add (self.pos_slider)
    self.on_forward_button = gtk.Button ("->")
    self.on_forward_button.connect("clicked", lambda *args: self.call_callbacks("forward"))
    hbox.add_with_properties(self.on_forward_button, "expand", False)

    self.movie_window.connect("button_press_event", self.on_movie_clicked)
    self.movie_window.set_events(gtk.gdk.BUTTON_PRESS_MASK)

    self.set_ui_state("STOP")
    window.show_all()
    self.iofn_hbox.hide ()

  def provide_movie_window_xid(self, setter):
    gtk.threads_enter()
    setter(self.movie_window.window.xid)
    gtk.threads_leave()

  def on_open(self, *args):
    chooser = gtk.FileChooserDialog(title = "Open", action = gtk.FILE_CHOOSER_ACTION_OPEN,
                                    buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    chooser.set_show_hidden (True)
    if (self.last_folder): chooser.set_current_folder (self.last_folder)
    filepath = None
    if chooser.run () == gtk.RESPONSE_OK:
      filepath = chooser.get_filename()
      self.last_folder = os.path.dirname(filepath)
    chooser.destroy()
    if filepath: self.call_callbacks("open", filepath)

  def playlist_mode(self, playlist_p, n = None):
    if playlist_p:
      self.ofn_label.set_text ("of " + str (n))
      self.iofn_spin.set_range (1, n)
      self.iofn_hbox.show ()
    else:
      self.iofn_hbox.hide()

  def set_iofn(self, i):
    print "set_iofn", i
    gtk.threads_enter()
    if i != self.get_iofn_pl_pos():
      self.iofn_spin.set_value (i)
    gtk.threads_leave()
  def get_iofn_pl_pos(self):
    return int (self.iofn_spin.get_value ())
  def on_iofn_changed(self, *args):
    i = self.get_iofn_pl_pos()
    self.call_callbacks("iofn_changed", i)
    return True

  def update_ui (self, pos):
    if self.jump_to is None:
      self.pos_slider.set_value (pos)

  def on_change_position1(self, *args):
    self.jump_to = self.pos_slider.get_value ()

  def on_change_position2(self, *args):
    if self.jump_to is not None:
      self.call_callbacks("seek_percent", self.jump_to)
      self.jump_to = None

  def on_movie_clicked(self, *args):
    self.toggle_controls()

  def toggle_controls(self, make_visible = None):
    if make_visible is None:
      make_visible = not self.control_panel.props.visible  # toggle
    if make_visible:
      self.control_panel.show()
      self.window.unfullscreen()
    else:
      self.control_panel.hide()
      self.window.fullscreen()

  def create_timer(self, interval, cb):
    return gobject.timeout_add_seconds (interval, cb)
  def cancel_timer(self, timer):
    gobject.source_remove(timer)
