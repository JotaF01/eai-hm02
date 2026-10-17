n = 2
term(t) = t**2 - 10*cos(2*pi*t)
sphere(a,b) = a**2 + b**2
rastrigin(a,b) = 10*n +term(a) +term(b)
f(name, a, b)=(name eq "sphere") ? sphere(a,b) : rastrigin(a, b)

set terminal pngcairo size 900,700 font ",11"
set xrange [-5.12:5.12]
set yrange [-5.12:5.12]
set xlabel "x1"
set ylabel "x2"
set palette cubehelix start 0.5 cycles -1.2 saturation 1.2
set cntrparam levels 14

do for [name in "sphere rastrigin"]{
    grid = (name eq "rastrigin")? 201:61
    set isosample grid,grid
    set samples grid,grid

    set output sprintf("plots/%s_surface.png",name)
    set title sprintf("%s, n=2: surface", name)
    set view 58, 35
    set size nosquare
    set pm3d
    set contour base
    unset key
    splot f(name, x, y) with pm3d

    set output sprintf("plots/%s_contour.png",name)
    set title sprintf("%s, n=2: contour map (top view)", name)
    set view map
    set size square
    splot f(name, x, y) with pm3d, f(name,x,y) with lines lc rgb "black" lw 0.6 nosurface
    unset pm3d
    unset contour
}