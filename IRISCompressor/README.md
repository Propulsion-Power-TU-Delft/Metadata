# IRIS Compressor

This folder contains the full set of design maps and the geometrical data of the optimal centrifugal compressor stage described in the paper 
"The Effect of Size and Working Fluid on the Multi-Objective Design of High-Speed Centrifugal Compressors". 

---

## Information

The impeller features 7 main blades and 7 seven splitter blade passages.
The geometry of the impeller and the diffuser are provided in ".crv" and ".igs" formats.
The ".crv" files can be directly imported in Ansys Turbogrid.
Alternatively, the ".igs" file can be opened in most of the CAD softwares.

---

## Constant Design Variables throughout the Maps
* Impeller shape factor = 0.9
* Diffuser radius ratio = 1.5
* Number of blades (main + splitter) = 14

---

## Design Point Boundary Conditions for CFD
* Fluid = R1233zd(E)
* Pt_in = 47.789 kPa
* Tt_in = 278.13 K
* mass flow rate = 114 g/s
* omega = 85.7 krpm

---

## Main Contributors
* **A. Giuffré**, PhD Researcher, Propulsion & Power, TU Delft - a.giuffre@tudelft.nl
* **M. Pini**, Assistant Professor, Propulsion & Power, TU Delft - m.pini@tudelft.nl