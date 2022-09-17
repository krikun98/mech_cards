import csv
import re
from io import TextIOWrapper
from typing import List


class Card:
    def __init__(self, row: List[str]): 
        self.nickname = Card.sanitize(row[0])
        self.boardname = Card.sanitize(row[1])
        self.revision = Card.sanitize(row[2])
        self.pcb = Card.sanitize(row[3])
        self.plate = Card.sanitize(row[4])
        self.switches = Card.sanitize(row[5])
        self.stabs = Card.sanitize(row[6])
        self.keycaps = Card.sanitize(row[7])
        if len(row) > 8:
            self.link = Card.sanitize(row[8])
        else:
            self.link = "https://t.me/rufrontier"

    def sanitize(word: str) -> str:
        """ From https://gist.github.com/jomigo96/6a040d4e4ad384bccd81c9a65e5cd210
        Sanitizes a string so that it can be properly compiled in TeX.
        Escapes the most common TeX special characters: ~^_#%${}
        Removes backslashes.
        """
        s = re.sub('\\\\', '', word)
        s = re.sub(r'([_^$%&#{}])', r'\\\1', s)
        s = re.sub(r'\~', r'\\~{}', s)
        if s == "":
            return "-"
        return s

    def print(self, file: TextIOWrapper):
        file.write("\t\\conventioncard{\@" + self.nickname +
        "}{" + self.boardname +
        "}{" + self.revision +
        "}{" + self.pcb +
        "}{" + self.plate +
        "}{" + self.switches +
        "}{" + self.stabs +
        "}{" + self.keycaps +
        "}{" + self.link + "}\n")

with open('main.tex', "w", encoding='utf-8') as outputfile:
    outputfile.write(r"""
\documentclass[a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[russian]{babel}
\usepackage{pdflscape}    
\usepackage{qrcode}
\usepackage{lmodern}

\usepackage[boxed]{ticket}
\usepackage[margin=10mm]{geometry}
\usepackage{graphicx}

\input{cards.tex}

\begin{document}
\begin{landscape}
""")

    with open('./data.csv', newline='', encoding='utf-8') as csvfile:
        cardreader = csv.reader(csvfile,dialect=csv.excel)
        for row in cardreader:
            Card(row).print(outputfile)
    
    outputfile.write(r"""
\end{landscape}
\end{document}
""")
