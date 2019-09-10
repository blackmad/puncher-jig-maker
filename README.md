# puncher-jig-maker

A tool for making custom rulers, and custom jigs for helping space rivet holes in leather.

I personally find it super useful to have a collection of rulers around that I know exactly how tall they are. These rulers end up being super useful for mindless spacing of cuts (in my case, often leather straps). It's hard to find commercial rulers that are thick enough to cut against, in the sizes I want, and sometimes they lie about the size (I bought a nice ruler advertised as 1" tall that was actually 1.125")

The tool assumes you're sending these to a laser cutter that likes 0.001pt #ff0000 lines for cuts, and black areas for engraving.

This tool requires the installation of pyfpdf from github, not pip https://github.com/reingart/pyfpdf


## Ruler maker

### Generates a ruler 10 cm high and 100 cm wide

    make_ruler.py -H 10 -w 100 -u cm
    
![100cm ruler](http://dump.blackmad.com.s3.amazonaws.com/rulers/ruler-10.0-x-100-cm.png)

### Generates a ruler 3/4 inch high and 12 inch wide

    make_ruler.py -H 0.75 -w 12 -u in 
    
![12in ruler](http://dump.blackmad.com.s3.amazonaws.com/rulers/ruler-0.75-x-12-in.png)


## Jig maker

These are likely only relevant to your life if you are me and are making leather accessories, but maybe you will find a use fo r them. 

More narrative explanation of how these are used: https://blackmad.com/leather-working/custom-jigs-rulers/

### Generate all jigs
    make_jigs.py
   
![3/4 rivet jig](http://dump.blackmad.com.s3.amazonaws.com/rulers/0.75_rivet_jigs.pdf.png)
