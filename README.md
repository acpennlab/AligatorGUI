# Aligator: Analysis of Ligand Gating: trains and other relaxations
Base code created and developed by Andrew Plested of FMP Berlin to model glutamate receptor gating
GUI coded and packaged by Samuel Liu and Andrew Penn and the University of Sussex
Aligator is distributed under a GPL-3.0 licence. See LICENCE.txt for more information.

The software is compiled for Windows (32-bit) and is expected to runs on Windows versions that support 32-bit and 64-bit applications, although this has not been extensively tested. To run the compiled windows application, unpack the zip file and double-click the Aligator.exe file in the 'Compiled' folder.

Running from source requires Python 2 and depends on:
PyQt5
matplotlib
numpy
importlib


Output for Aligator Gui are as follows:

timestamp_log.txt - Log file for excecution
timestamp_mechs.txt - File containing the mechanism for the given run (parameters in spinners)

output.png - Raster image of graph saved by matplotlib
output.eps - Encapsulated PostScript of graph saved by matplotlib
output.svg - Vector image of graph saved by matplotlib

train_mtempmech_linear.atf - ATF save of trace (usable in stimfit)
train_mtempmech_linear.itx - ITX save of trace (usable in igor)
train_mtempmech_linear.txt - Plain TXT save of trace

train_mtempmechrate.txt - File containing parameter that would have been changed multiple trials were to be done (Useless for GUI)
