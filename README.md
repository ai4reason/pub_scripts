SCRIPTS OUT DATED by [ai4reason/ai4reason.github.io](https://github.com/ai4reason/ai4reason.github.io)

How to update publications list in activities for AI4REASON
-----------------------------------------------------------

1) Use the script `pub-year-list.py` as follows:

   $ ./pub-year-list.py 2023 > bib-2023.html

   where `2023` is the year for which you want the publications.

Note: For Python 3 you need to uncomment import line with urlopen

2) The content of the output file `bib-2023.html` has to be inserted into the
file `activities.html` at the right position under the heading `Publications`.
Right after `<ol reversed>` insert `<h3>2023</h3>` and then the file content.

3) You might want to update the list of authors in the dictionary
`DBLP_AUTHORS` with their DBLP ids.

4) For export to CSV use:
   
   $ ./pub-year-list.py --csv 2023 > bib-2023.csv

