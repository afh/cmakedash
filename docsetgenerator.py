# docsetgenerator - a dash docset generator

import os
import shutil
import sqlite3
import plistlib
import argparse
import subprocess
import xml.etree.ElementTree as ET

class DocsetGenerator:
  def __init__(self):
    self.verbose = False
    self.docsetName = 'Unnamed'
    self.iconFilename = 'icon.png'

  def getargs(self):
    parser = argparse.ArgumentParser(description='cmakedash')
    parser.add_argument('-v', '--verbose',
        dest='verbose',
        action='store_true',
        help='show verbose information when generating the docset')
    parser.add_argument('feedurl',
        metavar='URL',
        nargs='*',
        help='include URL')
    return parser.parse_args()

  def generateHtml(self):
    pass

  def documentsPath(self):
    return os.path.join('build', '%s.docset' % (self.docsetName), 'Contents', 'Resources', 'Documents')

  def copyIcon(self):
    if (os.path.exists(self.iconFilename)):
      shutil.copy(self.iconFilename, os.path.join('build', '%s.docset' % (self.docsetName)))

  def createInfoPlist(self):
    infoPlist = dict(
        CFBundleIdentifier    = self.docsetName.lower(),
        DocSetPlatformFamily  = self.docsetName.lower(),
        CFBundleName          = self.docsetName,
        isDashDocset          = True,
        dashIndexFilePath     = 'index.html',
        );
    plistFile = os.path.join('build', '%s.docset' % (self.docsetName), 'Contents', 'Info.plist')
    plistlib.writePlist(infoPlist, plistFile)

  def generateFeed(self, feedurl):
    entry = ET.Element('entry')
    version = ET.SubElement(entry, 'version')
    version.text = self.dashFeedVersion()
    for url in feedurl:
      el = ET.SubElement(entry, 'url')
      el.text = url

    with open(os.path.join('build', '%s.xml' % (self.docsetName)), 'w') as fp:
      fp.write(ET.tostring(entry))

  def createArchive(self):
    os.system("tar --exclude='.DS_Store' -C build -czf build/%s.tgz %s.docset" % (self.docsetName, self.docsetName))

  def addIndexEntry(self, name, stype, path):
    self.db.cursor().execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, stype, path))
    if self.verbose: print 'name: %s, type: %s, path: %s' % (name, stype, path)

  def dbOpen(self):
    resourcesPath = os.path.dirname(self.documentsPath())
    self.db = sqlite3.connect(os.path.join(resourcesPath, 'docSet.dsidx'))
    cur = self.db.cursor()
    try: cur.execute('DROP TABLE searchIndex;')
    except: pass
    cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
    cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

  def dbClose(self):
    self.db.commit()
    self.db.close()

  def prepare(self):
    try: os.makedirs(self.documentsPath())
    except: pass

  def run(self, args):
    self.verbose = args.verbose
    if self.verbose: print 'Generating', self.docsetName, 'DocSet'
    self.prepare()
    self.copyIcon()
    self.createInfoPlist()
    self.generateHtml()
    self.dbOpen()
    self.generateIndex()
    self.dbClose()
    self.createArchive()
    self.generateFeed(args.feedurl)

