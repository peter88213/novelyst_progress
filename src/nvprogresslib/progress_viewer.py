"""Provide a tkinter widget for progress log display.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_collection
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from datetime import date
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
        columns = (
            'wordCount',
            'wordCountDelta',
            'totalWordCount',
            'totalWordCountDelta'
            )
        self.tree = ttk.Treeview(self, selectmode='none', columns=columns)
        scrollY = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollY.set)
        scrollY.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.heading('#0', text=_('Date'))
        self.tree.heading('wordCount', text=_('Word count'))
        self.tree.heading('wordCountDelta', text=_('Daily'))
        self.tree.heading('totalWordCount', text=_('With unused'))
        self.tree.heading('totalWordCountDelta', text=_('Daily'))

        self.tree.tag_configure('positive', foreground='black')
        self.tree.tag_configure('negative', foreground='red')
        self.isOpen = True
        self.build_tree()

    def on_quit(self, event=None):
        self._plugin.kwargs['window_geometry'] = self.winfo_geometry()
        self.destroy()
        self.isOpen = False

    def build_tree(self):
        wcLog = {}

        # Copy the read-in word count log.
        for wcDate in self._ui.prjFile.wcLog:
            wcLog[wcDate] = self._ui.prjFile.wcLog[wcDate]

        # Add the word count determined when opening the project.
        for wcDate in self._ui.prjFile.wcLogUpdate:
            wcLog[wcDate] = self._ui.prjFile.wcLogUpdate[wcDate]

        # Add the actual word count.
        newCountInt, newTotalCountInt = self._ui.prjFile.count_words()
        newCount = str(newCountInt)
        newTotalCount = str(newTotalCountInt)
        today = date.today().isoformat()
        wcLog[today] = [newCount, newTotalCount]

        lastCount = 0
        lastTotalCount = 0
        for wc in wcLog:
            columns = []
            nodeTags = ()
            countInt = int(wcLog[wc][0])
            countDiffInt = countInt - lastCount
            if countDiffInt > 0:
                nodeTags = ('positive')
            else:
                nodeTags = ('negative')
            totalCountInt = int(wcLog[wc][1])
            totalCountDiffInt = totalCountInt - lastTotalCount
            columns = [
                str(wcLog[wc][0]),
                str(countDiffInt),
                str(wcLog[wc][1]),
                str(totalCountDiffInt),
                ]
            lastCount = countInt
            lastTotalCount = totalCountInt
            self.tree.insert('', 'end', iid=wc, text=wc, values=columns, tags=nodeTags, open=True)
