# Bridge Activity

# Copyright (C) Sugar Labs

#  This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from gettext import gettext as _

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

import pygame
import sugargame.canvas

from gi.repository import Gtk
from gi.repository import Gdk

from sugar3.activity.activity import Activity
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.toggletoolbutton import ToggleToolButton
from sugar3.graphics.style import GRID_CELL_SIZE
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import StopButton
from helpbutton import HelpButton

import tools
from physics import PhysicsGame


class BridgeActivity(Activity):

    def __init__(self, handle):
        Activity.__init__(self, handle)

        self.game = PhysicsGame(activity=self)
        self.build_toolbar()
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self,
                             main=self.game.run,
                             modules=[pygame.display])

        w = Gdk.Screen.width()
        h = Gdk.Screen.height() - 2 * GRID_CELL_SIZE
        self._pygamecanvas.set_size_request(w, h)

        self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.grab_focus()

    def build_toolbar(self):
        self.max_participants = 1

        toolbar_box = ToolbarBox()

        activity_button = ActivityToolbarButton(self)

        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        self.blocklist = []
        self.radioList = {}
        for c in tools.allTools:
            button = ToolButton(c.icon)
            button.set_tooltip(_(c.toolTip))
            button.connect('clicked', self.radioClicked)
            toolbar_box.toolbar.insert(button, -1)
            button.show()
            self.radioList[button] = c.name

        self._pause = ToggleToolButton('media-playback-pause')
        self._pause.set_tooltip(_('Pause'))
        self._pause.connect('toggled', self._pause_play_cb)
        self._pause.show()
        toolbar_box.toolbar.insert(self._pause, -1)

        self._new_train = ToolButton('list-add')
        self._new_train.show()
        toolbar_box.toolbar.insert(self._new_train, -1)
        self._new_train.set_tooltip(_('Create a new train.'))
        self._new_train.connect('clicked', self.new_train_cb)
        self._new_train.show()

        self._restart = ToolButton('new-game')
        self._restart.show()
        toolbar_box.toolbar.insert(self._restart, -1)
        self._restart.set_tooltip(_('Restart'))
        self._restart.connect('clicked', self.restart_cb)
        
        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        helpbutton = self._create_help_button()
        toolbar_box.toolbar.insert(helpbutton, -1)
        helpbutton.show_all()


        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show_all()

    def radioClicked(self, button):
        evt = pygame.event.Event(
            pygame.USEREVENT, action=self.radioList[button])
        pygame.event.post(evt)

    def _pause_play_cb(self, button):
        self.game.pause_button_up()

    def new_train_cb(self, button):
        self.game.create_new_train_button_up()
    
    def restart_cb(self, button):
        self.game.restart_button_up()

    def _create_help_button(self):
        helpitem = HelpButton()

        helpitem.add_section(_('Useful commands'))
        helpitem.add_section(_('cd'))
        helpitem.add_paragraph(_('Change directory'))
        helpitem.add_paragraph(_('To use it, write: cd directory'))
        helpitem.add_paragraph(
            _('If you call it without parameters, will change\n'
              'to the user directory'))
        helpitem.add_section(_('ls'))
        helpitem.add_paragraph(_('List the content of a directory.'))
        helpitem.add_paragraph(_('To use it, write: ls directory'))
        helpitem.add_paragraph(
            _('If you call it without parameters, will list the\n'
              'working directory'))
        helpitem.add_section(_('cp'))
        helpitem.add_paragraph(_('Copy a file to a specific location'))
        helpitem.add_paragraph(_('Call it with the file and the new location'))
        helpitem.add_paragraph(_('Use: cp file directory'))
        helpitem.add_section(_('rm'))
        helpitem.add_paragraph(_('Removes a file in any path'))
        helpitem.add_paragraph(_('Use: rm file'))
        helpitem.add_section(_('su'))
        helpitem.add_paragraph(_('Login as superuser (root)'))
        helpitem.add_paragraph(
            _('The root user is the administrator of the\nsystem'))
        helpitem.add_paragraph(
            _('You must be careful, because you can modify\nsystem files'))

        return helpitem

    def read_file(self, file_path):
        self.game.read_file(file_path)

    def write_file(self, file_path):
        self.game.write_file(file_path)

    def get_preview(self):
        return self._pygamecanvas.get_preview()
