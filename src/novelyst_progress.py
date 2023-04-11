"""A daily progress log viewer plugin for novelyst.

Requires Python 3.6+
Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_progress
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from pathlib import Path
import webbrowser
from pywriter.config.configuration import Configuration
from pywriter.ui.set_icon_tk import *
from nvprogresslib.nvprogress_globals import *
from nvprogresslib.progress_viewer import ProgressViewer

SETTINGS = dict(
    window_geometry='510x440',
    date_width=100,
    wordcount_width=100,
    wordcount_delta_width=100,
    totalcount_width=100,
    totalcount_delta_width=100,
)
OPTIONS = {}


class Plugin:
    """novelyst daily progress log viewer plugin class.
    
    Public methods:
        disable_menu() -- disable menu entries when no project is open.
        enable_menu() -- enable menu entries when a project is open.    
    """
    VERSION = '@release'
    NOVELYST_API = '4.18'
    DESCRIPTION = 'A daily progress log viewer'
    URL = 'https://peter88213.github.io/novelyst_progress'

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self._ui.toolsMenu.entryconfig(APPLICATION, state='normal')

    def install(self, ui):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            ui -- reference to the NovelystTk instance of the application.
        """
        self._ui = ui
        self._progress_viewer = None

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/.pywriter/novelyst/config'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/progress.ini'
        self.configuration = Configuration(SETTINGS, OPTIONS)
        self.configuration.read(self.iniFile)
        self.kwargs = {}
        self.kwargs.update(self.configuration.settings)
        self.kwargs.update(self.configuration.options)

        # Create an entry in the Tools menu.
        self._ui.toolsMenu.add_command(label=APPLICATION, command=self._start_viewer)
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')

    def on_close(self):
        """Close the window."""
        self.on_quit()

    def on_quit(self):
        """Write back the configuration file."""
        if self._progress_viewer:
            if self._progress_viewer.isOpen:
                self._progress_viewer.on_quit()

        #--- Save configuration
        for keyword in self.kwargs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.kwargs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.kwargs[keyword]
        self.configuration.write(self.iniFile)

    def _start_viewer(self):
        if self._progress_viewer:
            if self._progress_viewer.isOpen:
                self._progress_viewer.lift()
                self._progress_viewer.focus()
                self._progress_viewer.build_tree()
                return

        self._progress_viewer = ProgressViewer(self, self._ui)
        self._progress_viewer.title(f'{self._ui.novel.title} - {PLUGIN}')
        set_icon(self._progress_viewer, icon='wLogo32', default=False)

