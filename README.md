# Sodium Conductor Project
### Chem 4PB3 - Winter 2024
##### Cameron Gurwell
<hr></hr>

<p>This repository is intended to hold the data collected for the final project and presentation in
the class <strong>Chem 4PB3</strong> (Computational Quantum)</p>

<p>The structure of the repo is very similar to the layout of the codespace I used on my home
PC to run the ML simulations. Most calculations and work was completed using an AMD Ryzen 3700x
CPU and an AMD Radeon 6800 GPU. For most standard applications of structure optimisation
(e.g. <strong>CASTEP, VASP, Quantum Espresso</strong>), a high powered supercomputer is necessary
to crunch the large amounts of data and numbers. This project was aimed at investigating the recent 
developments into low power structure optimisation using ML.</p>

<p><strong>MACE</strong>, the optimisation library used inside of <strong>Python</strong>, was developed
using the <strong>ASE</strong> framework and uses complex ANSATZ picking to construct wavefunctions. 
<strong>MACE-MP-0</strong>, the model used ontop of MACE, was developed by the 
<strong>Materials Project</strong> and <strong>MACE</strong> as a pretrained model to pick ANSATZ for 
89 elements on the periodic table.</p>

<p>This project used the above materials to create the below figure using structure optimisation
and a library called <strong>BVLain</strong> to construct sodium ion pathways through a novel conductor
intially developed by the <strong>Mozharivskyj Group</strong> and investigated by the 
<strong>Goward Group</strong>.</p>

<hr></hr>

### Na<sub>4</sub>Sn<sub>2</sub>Ge<sub>5</sub>O<sub>16</sub>

![Sodium Conductor with Channels](https://github.com/Camgur/4PB3_Sodium_Conductor/blob/89063e302fde4656a65c12b8e674236dbfd52be6/Figures/Na4Sn2Ge5O16.png)
