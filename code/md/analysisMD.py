import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from ase import io
'''
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

# Usage
traj_file = r'MACE\asemd\LSnPS\orb\md_300_0_opt_LSnPS.traj'  # Replace with your trajectory file path
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


temp = [300, 400, 500, 600]
# lagp
chgnet = [1.976e-10, 5.861e-10, 1.359e-9, 1.817e-9]
m3gnet = [2.770e-11, 2.825e-11, 1.283e-10, 2.985e-10]
mace = [1.189e-11, 2.249e-10, 6.173e-10, 1.117e-9]
orb = [3.832e-11, 1.132e-10, 4.229e-10, 6.383e-10]

# lgps
# chgnet = [1.234e-9, 2.020e-9, 3.121e-9, 4.922e-9]
# m3gnet = [1.848e-9, 3.722e-9, 6.603e-9, 1.010e-8, ]
# mace = [1.321e-10, 4.642e-10, 9.283e-10, 1.401e-9]
# orb = [2.501e-11, 1.964e-10, 9.212e-10, 1.325e-9, ]

# lsnps
# chgnet = [7.545e-10, 1.981e-9, 3.587e-9, 5.250e-9]
# m3gnet = [1.290e-9, 3.571e-9, 6.769e-9, 1.035e-8]
# mace = [8.948e-12, 2.183e-10, 6.236e-10, 1.101e-9]
# orb = [6.279e-11, 2.242e-10, 4.654e-10, 1.057e-9]




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
plt.savefig(r'MACE\asemd\LAGP\diffusion_LAGP.png')
plt.savefig(r'MACE\asemd\LAGP\diffusion_LAGP.svg')
# plt.show()

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
plt.savefig(r'MACE\asemd\LAGP\activation_LAGP.png')
plt.savefig(r'MACE\asemd\LAGP\activation_LAGP.svg')
# plt.show()
