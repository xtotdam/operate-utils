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
        if line.startswith('VERSION'):
            version = line.strip().split(' ')[-1]
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
    return (potentials, version)

def parse_last_values(lastvaluesfn, num=3):
    table = []
    for line in open(lastvaluesfn):
        l = line.strip().split(',')
        table.append(' & '.join(l) + ' \\\\\n')
    values = ''.join(table[-1-num:-1])
    print 'Parsed last values'
    return values

def parse_adatoms(adatomsfn):
    adatoms_number = 0
    adatoms_table = []
    coord_diff = []
    prev = None
    for line in open(adatomsfn):
        adatoms_number += 1
        adatoms_table.append(str(adatoms_number) + ' & ' + ' & '.join(line.strip().split(' ')[:-2]) + '\\\\\n')
        if prev:
            l = line.strip().split(' ')[0:3]
            p = prev.strip().split(' ')[0:3]
            coord_diff.append('{}\\rightarrow{} & {:+.6f} & {:+.6f} & {:+.6f} \\\\\n'.format(
                adatoms_number-1, adatoms_number,
                float(l[0]) - float(p[0]), float(l[1]) - float(p[1]), float(l[2]) - float(p[2])))
        prev = line
    print 'Parsed adatoms information'
    return (str(adatoms_number), ''.join(adatoms_table), ''.join(coord_diff))

def generate_latex_document(version, notes, values, header, config, potentials, adatoms_number, adatoms_table, coord_diff, finheader, boundcond, allatomsnumber):
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
    \usepackage{array}
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

    \section{Description}

    Version: \\texttt{''' + version + '''}


    ''' + notes + '''

    \section{Last energy values}
    \\begin{tabular}{l|l|l|l|l}
    $\Sigma$ E, meV & E$_R$, meV & E$_B$, meV & E$_{LR}$, meV & $\Delta$E, meV \\\\\hline
    '''
    + values +
    '''\hline
    \end{tabular}

    \section{Overall information}
    Header : `` ''' + header.replace('#','') + '''''\\\\

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
    \clearpage

    \section{Lattice information}
    Header : `` ''' + finheader.replace('#','') + '''''\\\\
    Number of atoms:\\ ''' + allatomsnumber + '''\\\\

    \\begin{tabular}{l|l|l|l}
    \hline ~ & x & y & z \\\\\hline
    Boundary conditions & ''' + boundcond + '''
    \end{tabular}\\\\

    \section{Adatoms information}
    Adatoms number: ''' + adatoms_number + '''\\\\

    \\begin{tabular}{l||l|l|l||l|l|l}
    \hline N & x & y & z & V$_x$ & V$_y$ & V$_z$ \\\\\hline
    '''
    + adatoms_table +
    '''
    \hline
    \end{tabular}\\\\

    \subsection{Coordinate differences}

    \\begin{tabular}{>{$}l<{$}|>{$}l<{$}|>{$}l<{$}|>{$}l<{$}}
    \hline n\\rightarrow(n-1) & x_n - x_{n-1} & y_n - y_{n-1} & z_n - z_{n-1} \\\\\hline
    '''
    + coord_diff +
    '''
    \hline
    \end{tabular}
    \clearpage

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
    from cellplot import generate_temp_fin

    finfilename = 'cu001.fin'
    rzfilename = 'cu001.rz'
    lastvaluesfn = '.lastvalues.csv'
    adatomsfn = '.adatoms.fin'

    while True:
        if exists(finfilename) and access(finfilename, R_OK): break
        else: finfilename = raw_input('Input fin filename: ')

    while True:
        if exists(rzfilename) and access(rzfilename, R_OK): break
        else: rzfilename = raw_input('Input rz filename: ')

    while True:
        if exists(lastvaluesfn) and access(lastvaluesfn, R_OK): break
        else: lastvaluesfn = raw_input('Input last values filename: ')

    while True:
        if exists(adatomsfn) and access(adatomsfn, R_OK): break
        else: adatomsfn = raw_input('Input adatoms coordinates and velocities filename: ')

    (ad, finheader, boundcond, allatomsnumber) = generate_temp_fin(finfilename)

    (rzfile, config, header) = parse_config(rzfilename)
    potentials = parse_potentials(rzfile)
    values = parse_last_values(lastvaluesfn, num=5)
    (adatoms_number, adatoms_table, coord_diff) = parse_adatoms(adatomsfn)
    notes = raw_input('Enter description/notes on this calculations: ')
    generate_latex_document(version, notes, values, header, config, potentials, adatoms_number, adatoms_table, coord_diff, finheader, boundcond, allatomsnumber)
