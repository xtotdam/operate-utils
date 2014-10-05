#! /usr/bin/python2
from os.path import exists
from os import access, R_OK

def generate_temp_fin(finfilename):
    stillatoms =  open('.still.fin', 'w')
    movingatoms = open('.moving.fin', 'w')
    adatoms =     open('.adatoms.fin', 'w')

    ad = []
    for line in open(finfilename):
        parts = filter(None, line.strip().split(' '))
        if len(parts) == 8:
            if int(parts[6]):
                adatoms.write(' '.join(parts) + '\n')
                ad.append([float(x) for x in parts[0:3]])
            elif int(parts[7]):
                movingatoms.write(' '.join(parts) + '\n')
            else:
                stillatoms.write(' '.join(parts) + '\n')

    stillatoms.close()
    movingatoms.close()
    adatoms.close()
    print 'Temp fin\'s generated'
    return ad

def generate_gnuplot_fin_template(ad, offset = 0.2, dticks = 10.):
    limits = [[min(x) - offset, max(x) + offset] for x in [[x[i] for x in ad] for i in xrange(3)]]
    diff = [(x[1] - x[0])/dticks for x in limits]

    gpl = open('.cell.gpl', 'w')
    axis = ('X', 'Y', 'Z')
    pairs = ((1, 0), (0, 2), (1, 2))

    gpl.write('''#! /usr/bin/gnuplot -persist

    set terminal png
    set encoding default
    set grid
    set view equal xy
    unset key
    ''')

    for i, j in pairs:
        gpl.write(
        '''
        # set title '{axi}-{axj} cell projection'
        set xlabel '{axi}, A'
        set ylabel '{axj}, A'
        set xtics 2 rotate by 270
        set ytics 2
        set output '{axi}{axj}.png'
        plot '.still.fin'   using {i}:{j} with points ls 7 ps 1 lc rgb "red", \\
             '.moving.fin'  using {i}:{j} with points ls 7 ps 1 lc rgb "black", \\
             '.adatoms.fin' using {i}:{j} with points ls 7 ps 1 lc rgb "blue"
        '''.format(**{'i':i+1, 'j':j+1, 'axi':axis[i], 'axj':axis[j]}) )

    pairs = ((0, 1), (0, 2), (1, 2))
    for i, j in pairs:
        gpl.write(
        '''
        # set title '{axi}-{axj} cell projection - adatoms'
        set xlabel '{axi}, A'
        set ylabel '{axj}, A'
        set xtics {diffi} rotate by 270
        set ytics {diffj}
        set xrange [{limli}:{limri}]
        set yrange [{limlj}:{limrj}]
        set output '{axi}{axj}a.png'
        plot '.still.fin'   using {i}:{j} with points ls 7 ps 1 lc rgb "red", \\
             '.moving.fin'  using {i}:{j} with points ls 7 ps 1 lc rgb "black", \\
             '.adatoms.fin' using {i}:{j} with points ls 7 ps 1 lc rgb "blue"
        '''.format(**{'i':i+1, 'j':j+1, 'axi':axis[i], 'axj':axis[j],
                      'limli':limits[i][0], 'limri':limits[i][1],
                      'limlj':limits[j][0], 'limrj':limits[j][1],
                      'diffi': diff[i],'diffj': diff[j]}) )

    gpl.close()
    print 'Gnuplot fin template created'

if __name__ == '__main__':
    finfilename = 'cu001.fin'
    while True:
        if exists(finfilename) and access(finfilename, R_OK):
            break
        else:
            finfilename = raw_input('Input fin filename: ')

    ad = generate_temp_fin(finfilename)
    generate_gnuplot_fin_template(ad)
