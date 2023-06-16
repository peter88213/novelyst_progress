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
            'date',
            'wordCount',
            'wordCountDelta',
            'totalWordCount',
            'totalWordCountDelta',
            'spacer',
            )
        self.tree = ttk.Treeview(self, selectmode='none', columns=columns)
        scrollY = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollY.set)
        scrollY.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.heading('date', text=_('Date'))
        self.tree.heading('wordCount', text=_('Word count'))
        self.tree.heading('wordCountDelta', text=_('Daily'))
        self.tree.heading('totalWordCount', text=_('With unused'))
        self.tree.heading('totalWordCountDelta', text=_('Daily'))
        self.tree.column('#0', width=0)
        self.tree.column('date', anchor=tk.CENTER, width=self._plugin.kwargs['date_width'], stretch=False)
        self.tree.column('wordCount', anchor=tk.CENTER, width=self._plugin.kwargs['wordcount_width'], stretch=False)
        self.tree.column('wordCountDelta', anchor=tk.CENTER, width=self._plugin.kwargs['wordcount_delta_width'], stretch=False)
        self.tree.column('totalWordCount', anchor=tk.CENTER, width=self._plugin.kwargs['totalcount_width'], stretch=False)
        self.tree.column('totalWordCountDelta', anchor=tk.CENTER, width=self._plugin.kwargs['totalcount_delta_width'], stretch=False)

        self.tree.tag_configure('positive', foreground='black')
        self.tree.tag_configure('negative', foreground='red')
        self.isOpen = True
        self.build_tree()

    def build_tree(self):
        self.reset_tree()
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
            totalCountInt = int(wcLog[wc][1])
            totalCountDiffInt = totalCountInt - lastTotalCount
            if countDiffInt == 0 and totalCountDiffInt == 0:
                continue

            if countDiffInt > 0:
                nodeTags = ('positive')
            else:
                nodeTags = ('negative')
            columns = [
                wc,
                str(wcLog[wc][0]),
                str(countDiffInt),
                str(wcLog[wc][1]),
                str(totalCountDiffInt),
                ]
            lastCount = countInt
            lastTotalCount = totalCountInt
            # startIndex = 'end'
            # chronological order
            startIndex = '0'
            # reverse order
            self.tree.insert('', startIndex, iid=wc, values=columns, tags=nodeTags, open=True)

    def on_quit(self, event=None):
        self._plugin.kwargs['window_geometry'] = self.winfo_geometry()
        self._plugin.kwargs['date_width'] = self.tree.column('date', 'width')
        self._plugin.kwargs['wordcount_width'] = self.tree.column('wordCount', 'width')
        self._plugin.kwargs['wordcount_delta_width'] = self.tree.column('wordCountDelta', 'width')
        self._plugin.kwargs['totalcount_width'] = self.tree.column('totalWordCount', 'width')
        self._plugin.kwargs['totalcount_delta_width'] = self.tree.column('totalWordCountDelta', 'width')
        self.destroy()
        self.isOpen = False

    def reset_tree(self):
        """Clear the displayed tree."""
        for child in self.tree.get_children(''):
            self.tree.delete(child)

