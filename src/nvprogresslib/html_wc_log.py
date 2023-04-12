"""Provide a class for HTML word count log file representation.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from urllib.parse import quote
from string import Template
from pywriter.pywriter_globals import *


class HtmlWcLog:
    """Class for HTML word count log file representation."""
    DESCRIPTION = 'HTML word count log'
    EXTENSION = '.html'
    SUFFIX = '_wordcount_log'

    _css_styles = '''<style type="text/css">
body {font-family: sans-serif}
p.title {font-size: larger; font-weight: bold}
td {padding: 10}
tr.heading {font-size:smaller; font-weight: bold; background-color:lightgray}
table {border-spacing: 0}
table, td {border: lightgrey solid 1px; vertical-align: top}
td.chtitle {font-weight: bold}
</style>
'''

    _fileHeader = f'''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>   
{_css_styles}
<title>{_('Word count log')} ($Title)</title>
</head>

<body>
<p class=title>$Title {_('by')} $AuthorName - {_('Word count log')}</p>
<table>
<tr class="heading">
<td class="chtitle">{_('Date')}</td>
<td>{_('Word count')}</td>
<td>{_('increment')}</td>
<td>{_('with unused')}</td>
<td>{_('increment')}</td>
</tr>
'''

    _wcDayTemplate = '''<tr>
<td>$Date</td>
<td>$Count</td>
<td>$CountIncrement</td>
<td>$TotalCount</td>
<td>$TotalCountIncrement</td>
</tr>
'''
    _fileFooter = '''</table>
</body>
</html>
'''

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.

        Positional arguments:
            filePath: str -- path to the file represented by the File instance.
            
        Optional arguments:
            kwargs -- keyword arguments to be used by subclasses.  
            
        Extends the superclass constructor.          
        """
        super().__init__()
        self.novel = None

        self._filePath = None
        # str
        # Path to the file. The setter only accepts files of a supported type as specified by EXTENSION.

        self.projectName = None
        # str
        # URL-coded file name without suffix and extension.

        self.projectPath = None
        # str
        # URL-coded path to the project directory.

        self.filePath = filePath

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, filePath):
        """Setter for the filePath instance variable.
                
        - Format the path string according to Python's requirements. 
        - Accept only filenames with the right suffix and extension.
        """
        if self.SUFFIX is not None:
            suffix = self.SUFFIX
        else:
            suffix = ''
        if filePath.lower().endswith(f'{suffix}{self.EXTENSION}'.lower()):
            self._filePath = filePath
            try:
                head, tail = os.path.split(os.path.realpath(filePath))
                # realpath() completes relative paths, but may not work on virtual file systems.
            except:
                head, tail = os.path.split(filePath)
            self.projectPath = quote(head.replace('\\', '/'), '/:')
            self.projectName = quote(tail.replace(f'{suffix}{self.EXTENSION}', ''))

    def write(self):
        """Write instance variables to the export file.
        
        Create a template-based output file. 
        Return a message in case of success.
        Raise the "Error" exception in case of error. 
        """
        text = self._get_text()
        backedUp = False
        if os.path.isfile(self.filePath):
            try:
                os.replace(self.filePath, f'{self.filePath}.bak')
            except:
                raise Error(f'{_("Cannot overwrite file")}: "{norm_path(self.filePath)}".')
            else:
                backedUp = True
        try:
            with open(self.filePath, 'w', encoding='utf-8') as f:
                f.write(text)
        except:
            if backedUp:
                os.replace(f'{self.filePath}.bak', self.filePath)
            raise Error(f'{_("Cannot write file")}: "{norm_path(self.filePath)}".')

    def _get_text(self):
        """Call all processing methods.
        
        Return a string to be written to the output file.
        This is a template method that can be extended or overridden by subclasses.
        """
        lines = []
        template = Template(self._fileHeader)
        lines.append(template.safe_substitute(self._get_fileHeaderMapping()))
        template = Template(self._wcDayTemplate)
        lastCount = 0
        lastTotalCount = 0
        for wc in self.wcLog:
            countInt = int(self.wcLog[wc][0])
            countDiffInt = countInt - lastCount
            totalCountInt = int(self.wcLog[wc][1])
            totalCountDiffInt = totalCountInt - lastTotalCount
            if countDiffInt == 0 and totalCountDiffInt == 0:
                continue

            if countDiffInt > 0:
                cc = 'green'
            else:
                cc = 'red'
            if totalCountDiffInt > 0:
                tcc = 'green'
            else:
                tcc = 'red'
            wcMap = dict(
                Date=wc,
                Count=self.wcLog[wc][0],
                CountIncrement=f'<font color={cc}>{countDiffInt}</font>',
                TotalCount=f'<font color=grey>{self.wcLog[wc][1]}</font>',
                TotalCountIncrement=f'<font color={tcc}>{totalCountDiffInt}</font>',
                )
            lastCount = countInt
            lastTotalCount = totalCountInt
            lines.append(template.safe_substitute(wcMap))
        lines.append(self._fileFooter)
        return ''.join(lines)

