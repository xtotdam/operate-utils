#! /usr/bin/python2
from os.path import exists
from os import access, R_OK

def parse_config(rzfilename):
    global rzfile
    rzfile = open(rzfilename)
    config = []
    for line in rzfile:
        if line.strip().startswith('#'):
            header = line
        else:
            if line.startswith('==='):
                break
            line = line.strip().split('     ')
            config.append(line[0] + ' & ' + line[-1] + ' \\\\\n')
    config = ''.join(config).replace('_','-')
    print 'Parsed config from RZ'
    return (rzfile, config, header)

def parse_potentials(rzfile):
    potvalues, paramsdesc, potnames = [], [], []
    for i, line in enumerate(rzfile):
        line = line.strip()
        if not i%2:
            line = line[:-1].split('[')
            potnames.append(line[0])
            l = line[1].split(',')
            paramsdesc.append(' & '.join(l) + ' \\\\\n')
        else:
            l = line.split(' ')
            potvalues.append(' & '.join(l) + ' \\\\\n')

    potentials = []
    for name, desc, val in zip(potnames, paramsdesc, potvalues):
        state = 'l|' * (len(desc.split('&')) - 1) + 'l'
        potentials.append('\item ' + name + '\n\n\\begin{tabular}{' + state + '}\n' + desc + '\hline ' + val + '\end{tabular}\n\n')
    potentials = ''.join(potentials)
    print 'Parsed potentias'
    return potentials

def parse_last_values(lastvaluesfn):
    table = []
    for line in open(lastvaluesfn):
        l = line.strip().split(',')
        table.append(' & '.join(l) + ' \\\\\n')
    values = ''.join(table[-4:-1])
    print 'Parsed last values'
    return values

def parse_adatoms(adatomsfn):
    adatoms_number = 0
    adatoms_table = []
    for line in open(adatomsfn):
        adatoms_number += 1
        adatoms_table.append(str(adatoms_number) + ' & ' + ' & '.join(line.strip().split(' ')[:-2]) + '\\\\\n')
    print 'Parsed adatoms information'
    return (str(adatoms_number), ''.join(adatoms_table))

def generate_latex_document(values, header, config, potentials, adatoms_number, adatoms_table):
    latex = open('report.tex', 'w')
    latex.write('''
    \documentclass[12pt]{article}
    \usepackage[T2A]{fontenc}
    \usepackage[utf8]{inputenc}
    \usepackage[russian,english]{babel}
    \usepackage[ddmmyyyy,hhmmss]{datetime}
    \usepackage{graphicx}
    \usepackage{geometry}
    \usepackage{hyperref}
    \usepackage[hypcap]{caption}

    \hypersetup{
        colorlinks,
        citecolor=black,
        filecolor=black,
        linkcolor=black,
        urlcolor=black
    }

    \geometry{left=1.5cm}
    \geometry{right=1.5cm}
    \geometry{top=1.5cm}
    \geometry{bottom=1.5cm}

    \\begin{document}
    \parindent=0cm
    \\today\ \currenttime \hfill New-Illumine Report
    \hrule

    \section{Last energy values}
    \\begin{tabular}{l|l|l|l|l}
    $\Sigma$ E, meV (\\ref{fig:sume})& E$_R$, meV (\\ref{fig:er})& E$_B$, meV (\\ref{fig:eb})& E$_{LR}$, meV & $\Delta$E, meV (\\ref{fig:diffe})\\\\\hline
    '''
    + values +
    '''\hline
    \end{tabular}

    \section{Overall information}
    '''
    + header.replace('#','') +
    '''
    \\begin{tabular}{l|l}
    \hline Value & Description \\\\\hline
    '''
    + config +
    '''\hline
    \end{tabular}

    \section{Potential parameters}
    \\begin{enumerate}
    '''
    + potentials +
    '''
    \end{enumerate}

    \section{Adatoms information}
    Adatoms number: '''
    + adatoms_number +
    '''
    \n\n\\begin{tabular}{l|l|l|l|l|l|l}
    \hline N & x & y & z & V$_x$ & V$_y$ & V$_z$ \\\\\hline
    '''
    + adatoms_table +
    '''
    \hline
    \end{tabular}
    \section{Energy graphs}

    \\addcontentsline{toc}{subsubsection}{Full energy}
    \\begin{figure}[h]
        \centering
        \includegraphics[width=\\textwidth]{sume.pdf}
        \caption{Full energy evolution \label{fig:sume}}
    \end{figure}

    \\addcontentsline{toc}{subsubsection}{Energy difference}
    \\begin{figure}[h]
        \centering
        \includegraphics[width=\\textwidth]{diffe.pdf}
        \caption{Full energy difference evolution \label{fig:diffe}}
    \end{figure}

    \\addcontentsline{toc}{subsubsection}{Repulsion energy}
    \\begin{figure}[h]
        \centering
        \includegraphics[width=\\textwidth]{er.pdf}
        \caption{Repulsion energy evolution \label{fig:er}}
    \end{figure}

    \\addcontentsline{toc}{subsubsection}{Binding energy}
    \\begin{figure}[h]
        \centering
        \includegraphics[width=\\textwidth]{eb.pdf}
        \caption{Binding energy evolution \label{fig:eb}}
    \end{figure}

    \\vfill
    \clearpage

    \section{Cell images}
    \subsection{Cell}

    \\addcontentsline{toc}{subsubsection}{Cell XY}
    \\begin{figure}[h]
        \centering
        \includegraphics[width=\\textwidth]{YX.pdf}
        \caption{Cell in XY projection \label{fig:cell:xy}}
    \end{figure}

    \\addcontentsline{toc}{subsubsection}{Cell XZ}
    \\begin{figure}[h]
        \centering
        \includegraphics[width=\\textwidth]{XZ.pdf}
        \caption{Cell in XZ projection \label{fig:cell:xz}}
    \end{figure}

    \\addcontentsline{toc}{subsubsection}{Cell YZ}
    \\begin{figure}[h]
        \centering
        \includegraphics[width=\\textwidth]{YZ.pdf}
        \caption{Cell in YZ projection \label{fig:cell:yz}}
    \end{figure}

    \clearpage
    \subsection{Adatoms}

    \\addcontentsline{toc}{subsubsection}{Adatoms XY}
    \\begin{figure}[h]
        \centering
        \includegraphics[width=\\textwidth]{XYa.pdf}
        \caption{Cell in XY projection (adatoms) \label{fig:adatoms:xy}}
    \end{figure}

    \\addcontentsline{toc}{subsubsection}{Adatoms XZ}
    \\begin{figure}[h]
        \centering
        \includegraphics[width=\\textwidth]{XZa.pdf}
        \caption{Cell in XZ projection (adatoms) \label{fig:adatoms:xz}}
    \end{figure}

    \\addcontentsline{toc}{subsubsection}{Adatoms YZ}
    \\begin{figure}[h]
        \centering
        \includegraphics[width=\\textwidth]{YZa.pdf}
        \caption{Cell in YZ projection (adatoms) \label{fig:adatoms:yz}}
    \end{figure}

    \end{document}
    ''')
    latex.close()
    print 'Latex document generated'

if __name__ == '__main__':

    rzfilename = 'cu001.rz'
    while True:
        if exists(rzfilename) and access(rzfilename, R_OK):
            break
        else:
            rzfilename = raw_input('Input rz filename: ')

    lastvaluesfn = '.lastvalues.csv'
    while True:
        if exists(lastvaluesfn) and access(lastvaluesfn, R_OK):
            break
        else:
            lastvaluesfn = raw_input('Input last values filename: ')

    adatomsfn = '.adatoms.fin'
    while True:
        if exists(adatomsfn) and access(adatomsfn, R_OK):
            break
        else:
            adatomsfn = raw_input('Input adatoms coordinates and velocities filename: ')

    (rzfile, config, header) = parse_config(rzfilename)
    potentials = parse_potentials(rzfile)
    values = parse_last_values(lastvaluesfn)
    (adatoms_number, adatoms_table) = parse_adatoms(adatomsfn)
    generate_latex_document(values, header, config, potentials, adatoms_number, adatoms_table)
