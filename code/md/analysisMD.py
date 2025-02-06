import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from ase import io

def calculate_msd(traj, atom_indices=None):
    """
    Calculate the Mean Squared Displacement (MSD) from a trajectory file.

    Parameters:
    traj_file: str
        Path to the trajectory file (e.g., .traj, .xyz, .lammps).
    atom_indices: list of int, optional
        Indices of atoms to track. If None, all atoms are used.

    Returns:
    msd: np.ndarray
        Array of MSD values at each time step.
    """

    # Number of frames in the trajectory
    n_frames = len(traj)

    # If specific atom indices are not provided, use all atoms
    if atom_indices is None:
        atoms = traj[0]
        atom_indices = range(len(atoms))  # Track all atoms
    else:
        atoms = traj[0]
    
    # Initialize arrays to store positions and MSD
    positions = np.zeros((n_frames, len(atom_indices), 3))
    
    # Extract atom positions for each frame
    for i, frame in enumerate(traj):
        positions[i] = frame.positions[atom_indices]

    # Calculate the MSD
    msd = np.zeros(n_frames)
    for t in range(1, n_frames):
        # Calculate displacement from the first frame for each atom
        displacement = positions[t] - positions[0]
        squared_displacement = np.sum(displacement**2, axis=1)
        
        # Compute the average MSD over all tracked atoms
        msd[t] = np.mean(squared_displacement)

    return msd
'''
# Usage
traj_file = r'MACE\asemd\LSnPS\chgnet\md_598_15_opt_LSnPS.traj'  # Replace with your trajectory file path
traj = io.Trajectory(traj_file)

# Set timestep between iterations
timestep = 200 #fs

# Set target element
element = 'Li'

# Set up indices for target element
indices = []
for i, atom in enumerate(traj[0]):
    if atom.symbol == element:
        indices.append(i)

msd = calculate_msd(traj, indices)

# Establish timeline in ps
timeline = np.linspace(0, (len(msd) - 1)*timestep/1000, len(msd))



# Run Diffusion Coeff
def calc_diff(msd, t=timeline):
    """
    Calculate the Diffusion Coefficient from Mean Squared Displacement (MSD).

    Parameters:
    msd: list
        Calculated values for the MSD.
    t: list
        Time used as the x axis.

    Returns:
    msd: np.ndarray
        Array of MSD values at each time step.
    """

    # Set up and fit
    reg = LinearRegression()
    reg.fit(t.reshape(-1,1), msd)

    y_pred = reg.predict(t.reshape(-1,1))

    return np.float64(reg.coef_/6), y_pred

# Run for diffusion
diffusion, diff_line = calc_diff(msd)
print('Diffusion Coefficient: ', str(diffusion), ' Å²/ps')
print('Diffusion Coefficient: ', str(diffusion*10**-8), ' m²/s')

# Plot the MSD
f, ax = plt.subplots()
plt.plot(timeline, msd)
plt.plot(timeline, diff_line, color='Purple', linestyle='dashed')
plt.xlabel('Time step (ps)')
plt.ylabel('MSD (Å²)')
plt.title('Mean Squared Displacement')
plt.text(0.05, 0.90, str('{:0.3e}'.format(diffusion)) + ' Å²/ps', transform = ax.transAxes)
plt.text(0.05, 0.85, str('{:0.3e}'.format(diffusion*10**-8)) + ' m²/s', transform = ax.transAxes)
plt.savefig(traj_file.replace('.traj', '.png'))
# plt.show()

'''


temp = [298, 398, 498, 598]
# lagp
# chgnet = [2.586e-10, 4.93e-10, 1.937e-9, 2.25e-9]
# m3gnet = [1.544e-11, None, 1.144e-10, 5.317e-10]
# mace = [1.734e-11, 1.196e-10, 6.069e-10, 1.233e-9]
# orb = [5.384e-11, 1.723e-10, 3.229e-10, 6.955e-10]

# lgps
# chgnet = [1.038e-9, 1.918e-9, 3.055e-9, 4.284e-9]
# m3gnet = [None, 4.408e-9, 6.624e-9, 1.037e-8, ]
# mace = [7.380e-11, 4.399e-10, 1.033e-9, 1.452e-9]
# orb = [2.212e-11, None, 6.704e-10, 1.335e-9, ]

# lsnps
chgnet = [7.088e-10, 1.828e-9, 3.28e-9, 5.833e-9]
m3gnet = [1.275e-9, None, 7.156e-9, 1.021e-8]
mace = [2.08e-11, 2.573e-10, 5.115e-10, 1.059e-9]
orb = [3.132e-11, 2.01e-10, 3.633e-10, 1.008e-9]




# Run Activation Calc
def calc_act(diffusion, t=temp):
    """
    Calculate the Diffusion Coefficient from Mean Squared Displacement (MSD).

    Parameters:
    msd: list
        Calculated values for the MSD.
    t: list
        Time used as the x axis.

    Returns:
    msd: np.ndarray
        Array of MSD values at each time step.
    """

    # Set up arrays
    t = 1000/np.array(t)
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    imp = imp.fit(np.array(diffusion).reshape(-1, 1))
    d = np.log(imp.transform(np.array(diffusion).reshape(-1, 1)).astype('float'))

    # Set up and fit
    reg = LinearRegression()
    reg.fit(t.reshape(-1,1), d)

    y_pred = reg.predict(t.reshape(-1,1))
    pred = -reg.coef_*1000
    pred = 1.381*(10e-23)*pred
    # print(pred)

    return np.float64(pred*624219725343321000), y_pred


ch_act, ch_pred = calc_act(chgnet)
m3_act, m3_pred = calc_act(m3gnet)
ma_act, ma_pred = calc_act(mace)
or_act, or_pred = calc_act(orb)




f, ax = plt.subplots()
plt.scatter(temp, chgnet, label='chgnet', color='Blue', marker='o', s=60)
plt.scatter(temp, m3gnet, label='m3gnet', color='Purple', marker='v', s=60)
plt.scatter(temp, mace, label='mace', color='Red', marker='s', s=60)
plt.scatter(temp, orb, label='orb', color='Orange', marker='D', s=60)
plt.xlabel('Temperature [K]', fontsize=16)
plt.ylabel('Diffusion [m²/s]', fontsize=16)
# plt.title('LSnPS Diffusion')
plt.legend()
plt.savefig(r'MACE\asemd\LSnPS\diff_LSnPS.png')
plt.show()

f, ax = plt.subplots()
plt.scatter(1000/np.array(temp), np.log(np.array(chgnet).astype('float')), label='chgnet', color='Blue', marker='o', s=60)
plt.scatter(1000/np.array(temp), np.log(np.array(m3gnet).astype('float')), label='m3gnet', color='Purple', marker='v', s=60)
plt.scatter(1000/np.array(temp), np.log(np.array(mace).astype('float')), label='mace', color='Red', marker='s', s=60)
plt.scatter(1000/np.array(temp), np.log(np.array(orb).astype('float')), label='orb', color='Orange', marker='D', s=60)
plt.plot(1000/np.array(temp), ch_pred, color='Blue', linestyle='solid')
plt.plot(1000/np.array(temp), m3_pred, color='Purple', linestyle='dashed')
plt.plot(1000/np.array(temp), ma_pred, color='Red', linestyle='dotted')
plt.plot(1000/np.array(temp), or_pred, color='Orange', linestyle='dashdot')
plt.text(0.70, 0.92, 'chgnet: ' + str(round(ch_act, 3)) + ' eV', transform = ax.transAxes)
plt.text(0.70, 0.87, 'm3gnet: ' + str(round(m3_act, 3)) + ' eV', transform = ax.transAxes)
plt.text(0.70, 0.82, 'mace: ' + str(round(ma_act, 3)) + ' eV', transform = ax.transAxes)
plt.text(0.70, 0.77, 'orb: ' + str(round(or_act, 3)) + ' eV', transform = ax.transAxes)
plt.xlabel('1000/T [1/K]', fontsize=16)
plt.ylabel('ln(D)', fontsize=16)
# plt.title('LSnPS Diffusion')
plt.legend()
plt.savefig(r'MACE\asemd\LSnPS\activation_LSnPS.png')
plt.savefig(r'MACE\asemd\LSnPS\activation_LSnPS.svg')
plt.show()