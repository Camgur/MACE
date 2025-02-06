 set encoding iso_8859_1
set xlabel "Reaction coordinate / arb. u."
set ylabel "E - E_{IS} / eV"
set format y "%.2f"

set grid xtics ytics

set xzeroaxis lt -1
plot  [0:1][:] \
      'LiAlO2_neb.int' notitle w l lt 2 lw 4, \
      'LiAlO2_neb.dat' notitle w points lt 1 pt 7 ps 1.5
pause -1
