"""Provide a tkinter widget for progress log display.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_collection
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import tkinter as tk
from tkinter import ttk
from nvprogresslib.nvprogress_globals import *


class ProgressViewer(tk.Toplevel):
    _KEY_QUIT_PROGRAM = ('<Control-q>', 'Ctrl-Q')

    def __init__(self, plugin, ui):
        self._ui = ui
        self._plugin = plugin
        super().__init__()

        self.geometry(self._plugin.kwargs['window_geometry'])
        self.lift()
        self.protocol("WM_DELETE_WINDOW", self.on_quit)
        self.bind(self._KEY_QUIT_PROGRAM[0], self.on_quit)

        #--- Tree for log view.
        self.tree = ttk.Treeview(self, selectmode='browse')
        scrollY = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollY.set)
        scrollY.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.isOpen = True

    def on_quit(self, event=None):
        self._plugin.kwargs['window_geometry'] = self.winfo_geometry()
        self.destroy()
        self.isOpen = False

