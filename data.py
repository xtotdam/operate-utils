#! /usr/bin/python2

# energy.csv transformation
#
outsum = open('.sum.energy.dat', 'w')
outdif = open('.dif.energy.dat', 'w')
outenr = open('.enr.energy.dat', 'w')
outenb = open('.enb.energy.dat', 'w')

num_lines = sum(1 for line in open('energy.csv'))
offset = min(500, num_lines / 2)

for i, line in enumerate(open('energy.csv')):
    line = line.strip().split(',')
    if i > offset:
        outdif.write(str(i) + ',' + line[4] + '\n')
    outsum.write(str(i) + ',' + line[0] + '\n')
    outenr.write(str(i) + ',' + line[1] + '\n')
    outenb.write(str(i) + ',' + line[2] + '\n')

for p in (outsum, outdif, outenr, outenb):
    p.close()

# gnuplot templates
#
sumgr = open('.sum.gnuplot', 'w')
difgr = open('.dif.gnuplot', 'w')
enrgr = open('.enr.gnuplot', 'w')
enbgr = open('.enb.gnuplot', 'w')
xlabel = r'TD steps'
titles = (r'{/Symbol S}E', r'{/Symbol D}E', r'E_R', r'E_B')
filenames = ('sume.pdf', 'diffe.pdf', 'er.pdf', 'eb.pdf')
inputfiles = ('.sum.energy.dat', '.dif.energy.dat', '.enr.energy.dat', '.enb.energy.dat')
colors = ('black', 'red', 'blue', 'green')

for i, p in enumerate((sumgr, difgr, enrgr, enbgr)):
    p.write('''
#! /usr/bin/gnuplot -persist
set terminal pdf enhanced
set encoding utf8
set datafile separator ","
set xlabel '{xlabel}'
set grid
unset key

set title '{title}'
set ylabel '{title}, meV'
set output '{filename}'
plot '{inputfile}' using 1:2 with lines lw 2 lc rgb "{color}"
'''.format(xlabel=xlabel, title=titles[i], filename=filenames[i], inputfile=inputfiles[i], color=colors[i]))
    p.close()

# latex template

rzfile = open('cu001.rz')
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

potvalues, paramsdesc, potnames = [], [], []
for i, line in enumerate(rzfile):
    line = line.strip()
    if not i%2:
        line = line[:-1].split('[')
        potnames.append(line[0])
        l = line[1].split(',')
        paramsdesc.append(''.join([x + ' & ' if x is not l[-1] else x for x in l])+' \\\\\n')
    else:
        l = line.split(' ')
        potvalues.append(''.join([x + ' & ' if x is not l[-1] else x for x in l])+' \\\\\n')

potentials = []
for name, desc, val in zip(potnames, paramsdesc, potvalues):
    state = 'l|'*(len(desc.split('&'))-1)+'l'
    potentials.append('\item ' + name + '\n\n\\begin{tabular}{' + state + '}\n' + desc + '\hline ' + val + '\end{tabular}\n\n')
potentials = ''.join(potentials)

table = []
for line in open('.lastlines.csv'):
    l = line.strip().split(',')
    table.append(''.join([x + ' & ' if x is not l[-1] else x for x in l])+' \\\\\n')
values = ''.join(table[-4:-1])

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
\section{Energy graphs}
\\begin{figure}[h]
    \centering
    \includegraphics[width=\\textwidth]{sume.pdf}
    \caption{Full energy evolution \label{fig:sume}}
\end{figure}

\\begin{figure}[h]
    \centering
    \includegraphics[width=\\textwidth]{diffe.pdf}
    \caption{Full energy difference evolution \label{fig:diffe}}
\end{figure}

\\begin{figure}[h]
    \centering
    \includegraphics[width=\\textwidth]{er.pdf}
    \caption{Repulsive energy evolution \label{fig:er}}
\end{figure}

\\begin{figure}[h]
    \centering
    \includegraphics[width=\\textwidth]{eb.pdf}
    \caption{Binding energy evolution \label{fig:eb}}
\end{figure}
\\vfill
\clearpage
\section{Cell images}

To be added soon
\\begin{figure}[h]
    \centering
    \includegraphics[width=\\textwidth]{sume.pdf}
    \caption{Dummy picture \label{fig:sume}}
\end{figure}
\end{document}
''')
latex.close()
