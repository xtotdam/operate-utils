#! /usr/bin/python2

from os.path import exists
from os import access, R_OK
from cellplot import generate_temp_fin, generate_gnuplot_fin_template
from energyplot import generate_temp_csv, generate_gnuplot_energy_template
from latexdocument import parse_config, parse_potentials, parse_last_values, parse_adatoms, generate_latex_document

finfilename = 'cu001.fin'
energyfn = 'energy.csv'
rzfilename = 'cu001.rz'
lastvaluesfn = '.lastvalues.csv'
adatomsfn = '.adatoms.fin'

while True:
    if exists(finfilename) and access(finfilename, R_OK): break
    else: finfilename = raw_input('Input fin filename: ')

while True:
    if exists(energyfn) and access(energyfn, R_OK): break
    else: energyfn = raw_input('Input energy filename: ')

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
generate_gnuplot_fin_template(ad)

generate_temp_csv(energyfn)
generate_gnuplot_energy_template()

(rzfile, config, header) = parse_config(rzfilename)
potentials, version = parse_potentials(rzfile)
values = parse_last_values(lastvaluesfn)
(adatoms_number, adatoms_table, coord_diff) = parse_adatoms(adatomsfn)
notes = raw_input('Enter description/notes on this calculations: ')
generate_latex_document(version, notes, values, header, config, potentials, adatoms_number, adatoms_table, coord_diff, finheader, boundcond, allatomsnumber)
