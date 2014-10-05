#! /usr/bin/python2

def generate_temp_csv(energyfn):
    outsum = open('.sum.energy.dat', 'w')
    outdif = open('.dif.energy.dat', 'w')
    outenr = open('.enr.energy.dat', 'w')
    outenb = open('.enb.energy.dat', 'w')

    num_lines = sum(1 for line in open('energy.csv'))
    offset = min(500, num_lines / 2)

    for i, line in enumerate(open('energy.csv')):
        line = line.strip().split(',')

        if i > offset:
            outdif.write(str(i) + ' ' + line[4] + '\n')

        outsum.write(str(i) + ' ' + line[0] + '\n')
        outenr.write(str(i) + ' ' + line[1] + '\n')
        outenb.write(str(i) + ' ' + line[2] + '\n')

    for p in (outsum, outdif, outenr, outenb):
        p.close()
    print 'Temp csv\'s generated'

def generate_gnuplot_energy_plot():
    gpl = open('.energy.gpl', 'w')
    titles = ('{/Symbol S}E', '{/Symbol D}E', 'E_R', 'E_B')
    filenames = ('sume.pdf', 'diffe.pdf', 'er.pdf', 'eb.pdf')
    inputfiles = ('.sum.energy.dat', '.dif.energy.dat', '.enr.energy.dat', '.enb.energy.dat')
    colors = ('black', 'red', 'blue', 'green')

    gpl.write('''#! /usr/bin/gnuplot -persist

    set terminal pdf enhanced
    set encoding utf8
    set xlabel '{xlabel}'
    set grid
    unset key
    ''')

    for i in xrange(4):
        gpl.write(
        '''
        set title '{title}'
        set ylabel '{title}, meV'
        set output '{filename}'
        plot '{inputfile}' using 1:2 with lines lw 2 lc rgb '{color}
        '''.format(**{'title':titles[i], 'filename':filenames[i], 'inputfile':inputfiles[i], 'color':colors[i]}) )
    gpl.close()
    print 'Gnuplot energy template created'

if __name__ == '__main__':
    energyfn = raw_input('Input energy filename: ')
    generate_temp_csv(energyfn)
    generate_gnuplot_energy_plot()
