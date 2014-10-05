tail energy.csv > .lastvalues.csv

python energyplot.py
python cellplot.py

gnuplot .cell.gpl
gnuplot .energy.gpl

python latexdocument.py

pdflatex report.tex
pdflatex report.tex

del .still.fin .moving.fin .adatoms.fin
del .cell.gpl .energy.gpl
del .lastvalues.csv
del .sum.energy.dat .dif.energy.dat .enr.energy.dat .enb.energy.dat
del report.aux report.log report.out report.synctex.gz

tar -cf results.tar YX.pdf XZ.pdf YZ.pdf XYa.pdf XZa.pdf YZa.pdf sume.pdf diffe.pdf er.pdf eb.pdf energy.csv cu001.fin cu001.rz report.tex

del YX.pdf XZ.pdf YZ.pdf XYa.pdf XZa.pdf YZa.pdf sume.pdf diffe.pdf er.pdf eb.pdf energy.csv cu001.fin cu001.rz report.tex
