#!/usr/bin/env bash

python data.py
tail energy.csv > .lastlines.csv

gnuplot .sum.gnuplot
gnuplot .dif.gnuplot
gnuplot .enr.gnuplot
gnuplot .enb.gnuplot

pdftk sume.pdf diffe.pdf er.pdf eb.pdf cat output energies.pdf

pdflatex report.tex
pdflatex report.tex

rm .lastlines.csv
rm .sum.energy.dat .dif.energy.dat .enr.energy.dat .enb.energy.dat
rm .sum.gnuplot .dif.gnuplot .enr.gnuplot .enb.gnuplot
rm report.aux report.log report.out
