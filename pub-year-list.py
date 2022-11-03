#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sys
try:
   from urllib.request import urlopen # for Python 3
except ImportError:
   from urllib2 import urlopen # for Python 2

DBLP_AUTHORS = { 
   'Josef': '63/5214',
   'Karel': '39/11138',
   'Jan': '88/7998',
   'Martin': '24/5175-1',
   'Chad': '51/552',
   'Thibault': '146/0608',
   'Zar': '263/3219',
   'Bartosz': '215/3912',
   'Yutaka': '21/607',
   'Mikolas': '56/2424',
   'Lasse': '261/3275',
   'Jan Hula': '200/9929',
   'Tomas Mikolov': '45/8055',
   'Filip': '281/5411',
   'Barbora Hudcova': '298/8255',
   'Jelle': '285/5325',
   'Robert': '65/1151',
   'Erik': '211/3939',
   'Jiri Kubalik': '05/659',
   'Jan Zahalka': '54/9476',
   'Baran': '180/8715'
   #'Shawn': '58/3833',
   #'Filip': '?/?',
   #'Jirka': '66/1279',
}

HTML = """<li>
<div class="author">%s</div>
   <div class="title">%s</div>
   <div class="journal">%s</div>
   <div class="links">%s</div>
</li>
"""

RIS = re.compile(r"^([A-Z][A-Z0-9])  - (.*)$")

def parse(ris, year):
   db = {}
   entry = {}
   for line in ris.split("\n"):
      mo = RIS.match(line)
      if not mo:
         if entry:
            if int(entry["PY"].rstrip("/")) == year:
               db[entry["ID"]] = entry
               #print("FOUND "+entry["ID"])
            entry = {}
         continue
      if mo.group(1) == "AU" or mo.group(1) == "ED":
         if "AU" not in entry:
            entry["AU"] = []
         entry["AU"].append(mo.group(2))
      else:
         entry[mo.group(1)] = mo.group(2)
   return db

def fields(entry):
   authors = entry["AU"]
   authors = [" ".join(reversed(author.split(", "))) for author in authors]
   authors = ", ".join(authors) + "."

   title = entry["TI"]

   if entry["TY"] == "Informal Publication":
      journal = "arXiv %s %s (%s)." % (entry["JO"], entry["VL"], entry["PY"].rstrip("/"))
   elif entry["TY"] == "CPAPER":
      if "SP" in entry and "EP" in entry:
         journal = "%s: %s-%s (%s)." % (entry["BT"], entry["SP"], entry["EP"], entry["PY"].rstrip("/"))
      else:
         journal = "%s: (%s)." % (entry["BT"], entry["PY"].rstrip("/"))
   elif entry["TY"] == "JOUR":
      if "SP" in entry and "EP" in entry:
         journal = "%s %s: %s-%s (%s)." % (entry["JO"], entry["VL"], entry["SP"], entry["EP"], entry["PY"].rstrip("/"))
      else:
         journal = "%s %s: (%s)." % (entry["JO"], entry["VL"], entry["PY"].rstrip("/"))
   elif entry["TY"] == "CONF":
      journal = "%s %s (%s)." % (entry["T3"], entry["VL"], entry["PY"].rstrip("/"))
   elif entry["TY"] == "CHAP":
      journal = "%s: %s-%s (%s)." % (entry["BT"], entry["SP"], entry["EP"], entry["PY"].rstrip("/"))
   else:
      journal = "YAN TODO: " + entry["TY"]

   if "arxiv" in entry["UR"]:
      linkname = "arXiv"
   elif "doi" in entry["UR"]:
      linkname = "doi"
   elif "easychair" in entry["UR"]:
      linkname = "easychair"
   else:
      linkname = "url"
   links = '[ <a href="https://dblp.uni-trier.de/rec/%s.html?view=bibtex">BibTeX</a> | <a href="%s">%s</a> | <a href="http://dblp.uni-trier.de/rec/html/%s">dblp</a> ]' % (entry["ID"].split(":")[1], entry["UR"], linkname, entry["ID"].split(":")[1])

   return (authors, title, journal, links)

def html(entry):
   (authors, title, journal, links) = fields(entry)
   sys.stdout.write((HTML % (authors,title,journal,links)))

def csv(entry):
   (authors, title, journal, links) = fields(entry)
   sys.stdout.write(("%s; %s; %s\n" % (authors,title,journal)))

def publications(year, htmlmode=True):
   ris = ""
   for author in DBLP_AUTHORS:
      sys.stderr.write("Donwloading %s\n" % author)
      #url = "http://dblp.org/pid/%s.ris" % DBLP_AUTHORS[author]
      url = "https://dblp.uni-trier.de/pid/%s.ris" % DBLP_AUTHORS[author]
      data = urlopen(url)
      ris += data.read().decode("utf-8")

   db = parse(ris, year)
   sys.stderr.write("Relevant entries found: %d\n" % len(db))

   for entry in db.values():
      if htmlmode:
      	 html(entry)
      else:
         csv(entry)

if len(sys.argv) < 2:
   sys.stdout.write("usage: %s year\n" % sys.argv[0])
else:
   if len(sys.argv) == 3:
      htmlmode = sys.argv[1] != "--csv"
      year = int(sys.argv[2])
   else:
      htmlmode = True
      year = int(sys.argv[1])
   publications(year, htmlmode)

