#!/usr/bin/env python
#
# cmakedash - a dash docset generator for CMake

import os
import re
import subprocess
from bs4 import BeautifulSoup, NavigableString, Tag
from docsetgenerator import DocsetGenerator

class CMakeDocsetGenerator (DocsetGenerator):
  def __init__(self):
    DocsetGenerator.__init__(self)
    self.docsetName = 'CMake'
    self.iconFilename = 'icon.tiff'

  def helpFilename(self):
    return os.path.join(self.documentsPath(), 'index.html')

  def dashFeedVersion(self):
    cmakeVersion = subprocess.check_output('cmake --version'.split()).split()
    return cmakeVersion[2]

  def generateHtml(self):
    os.system("cmake --help-html > '%s'" % (self.helpFilename()))

  def generateIndex(self):
    page = open(self.helpFilename()).read()
    soup = BeautifulSoup(page)

    any = re.compile('.*')
    for tag in soup.find_all('a', {'href':any}):
      name = tag.text.strip()
      if len(name) > 0:
        path = tag.attrs['href'].strip()
        if path.startswith('#command'):
          stype = 'Command'
        elif path.startswith('#opt'):
          stype = 'Option'
        elif path.startswith('#variable'):
          stype = 'Variable'
        elif path.startswith('#module'):
          stype = 'Module'
        elif path.startswith('#prop_') or path.startswith('#property'):
          stype = 'Property'
        elif path.startswith('http'):
          continue
        else:
          if self.verbose: print 'Skipping %s' % (path)
          continue

        path = 'index.html%s' % (path)

        self.addIndexEntry(name, stype, path)

if __name__ == '__main__':
  generator = CMakeDocsetGenerator()
  args = generator.getargs()
  generator.run(args)
