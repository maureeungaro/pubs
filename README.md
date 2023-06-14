# pi0_resonance_regions


The `makeNote` script will create a `pi0.tex` using the 
`header.tex` and `pi0_content.tex` files, then run scons to compile the pdf.

The  (editable) `pi0_content.tex` file loads the following:

```
\include{electron_pid_content}
\include{proton_pid_content}
\include{vertex_content}
\include{electron_fiducial_content}
```
 

Each chapter can also be compiled individually by the local SConstruct, which:

1. Forms a tex file, typically from the top level `header.tex` and a 
`_standalone.tex` file
2. Copy the necessary images from the `mauriPlots` repo, 
using the `copy_images.sh` script
3. Compiles the pdf 

In turn, the `_standalone.tex` file loads the `_content.tex` file,
containing the individual subsections, and the bibliography file.
