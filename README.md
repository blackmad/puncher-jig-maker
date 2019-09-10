# puncher-jig-maker

A tool for making custom rulers, and custom jigs for helping space rivet holes in leather.

This tool requires the installation of pyfpdf from github, not pip https://github.com/reingart/pyfpdf

## Ruler maker

### Generates a ruler 10 cm high and 100 cm wide

    make_ruler.py -H 10 -w 100 -u cm
    
![100cm ruler](http://dump.blackmad.com.s3.amazonaws.com/rulers/ruler-10.0-x-100-cm.png)

### Generates a ruler 3/4 inch high and 12 inch wide

    make_ruler.py -H 0.75 -w 12 -u in 
    
![12in ruler](http://dump.blackmad.com.s3.amazonaws.com/rulers/ruler-0.75-x-12-in.png)
