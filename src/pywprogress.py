"""A test application for the novelyst_progress plugin.

For further information see https://github.com/peter88213/novelyst_progress
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from pywriter.pywriter_globals import *
from pywriter.ui.main_tk import MainTk
from novelyst_progress import Plugin

APPLICATION = 'View daily progress log'


class ProgressTk(MainTk):

    def __init__(self):
        kwargs = {
                'root_geometry': '800x500',
                'yw_last_open': '',
                'color_text_bg':'white',
                'color_text_fg':'black',
                }
        super().__init__(APPLICATION, **kwargs)
        self.toolsMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Tools'), menu=self.toolsMenu)
        self.helpMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Help'), menu=self.helpMenu)
        self.plugin = Plugin()
        self.plugin.install(self)

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        super().disable_menu()
        self.plugin.disable_menu()

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        super().enable_menu()
        self.plugin.enable_menu()


if __name__ == '__main__':
    ui = ProgressTk()
    ui.start()

