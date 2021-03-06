#! /usr/bin/python2
# coding=utf8

from operate_utils import generate_energy_plots_templates as gept, \
                          generate_lattice_plots_templates as glpt, \
                          parse_mcrd as pm, \
                          parse_last_values as plv, \
                          parse_adatoms as pa, \
                          generate_latex_document as gld

from glob import glob
from os.path import getctime
from os import system, remove, rename
from time import ctime
from sys import argv

if '--help' in argv:
    print '''
    Operate-utils
        By default compiles data to report
        -a   archives everything to compile on another machine'''
    exit(0)

enprefixes = ['sum', 'dif', 'enr', 'enb']
finprefixes = ['still','mov','adatom']
lastvaluesfn = '.lastvalues.csv'
num = 3

mcrfiles = glob('*.mcrd')
if not len(mcrfiles): print 'No machine-read files found! Now exit!'
elif len(mcrfiles) == 1: mcrf = mcrfiles[0]
else:
    for i, fn in enumerate(mcrfiles): print '{}: {} - {}'.format(i + 1, fn.ljust(25), ctime(getctime(fn)))
    num = int(raw_input('Choose the desired one. '))
    mcrf = mcrfiles[num - 1]

machreadinfo = pm(mcrf)
gept(machreadinfo['energycsv'], enprefixes)
glpt(machreadinfo['latticefin'], finprefixes)
system('tail -n {} {} > {}'.format(num, machreadinfo['energycsv'], lastvaluesfn))
values = plv(lastvaluesfn)
(adatoms_number, adatoms_table, coord_diff) = pa('.' + finprefixes[2] + '.fin')
notes = raw_input('Enter description/notes on this calculations: ')
gld(machreadinfo, notes, values, adatoms_number, adatoms_table, coord_diff, enprefixes)

s = open('compile.cmd', 'w')
s.write('gnuplot .cell.gpl\ngnuplot .energy.gpl\npdflatex report.tex\npdflatex report.tex')
s.close()
s = open('compile.sh', 'w')
s.write('gnuplot .cell.gpl\ngnuplot .energy.gpl\npdflatex report.tex\npdflatex report.tex')
s.close()
files = ['.' + prefix + '.energy.dat' for prefix in enprefixes] + ['.' + prefix + '.fin' for prefix in finprefixes] + \
        ['.cell.gpl', '.energy.gpl', 'report.tex', 'compile.cmd', 'compile.sh']
system('tar -cf non-compiled.tar ' + ' '.join(files + ['dummy.pdf']))
for f in files + ['.lastvalues.csv']:
    remove(f)
