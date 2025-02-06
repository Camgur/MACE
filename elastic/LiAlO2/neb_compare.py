import matplotlib.pyplot as plt
import numpy as np

qe = np.array([-3756.2572, -3756.0899, -3755.9920, -3755.5793, -3755.6760, -3756.0464, -3756.2572]) + 3756.2572
# qe = qe + 3756.2572
qe1 = list(reversed(qe))
qe2 = np.linspace(0, 6, 7)

chg1 = np.array([-104.7300, -104.6449, -104.5957, -104.4914, -104.3577, -104.3127, -104.3610, -104.4601, -104.5590, -104.6231, -104.6306, -104.7300]) + 104.7300
chg2 = np.linspace(0, 6, 12)

mac1 = np.array([-99.4912, -99.4049, -99.2890, -99.0668, -98.9447, -98.9977, -99.1137, -99.2449, -99.3414, -99.3863, -99.3760, -99.4912]) + 99.4912
mac2 = np.linspace(0, 6, 12)

print(chg1)

plt.plot(qe2, qe1, color='black', linestyle='solid', label='DFT', linewidth=3)
plt.plot(chg2, chg1, color='red', linestyle='dotted', label='CHGNet', linewidth=3)
plt.plot(mac2, mac1, color='blue', linestyle='dashed', label='MACE', linewidth=3)
plt.legend()
plt.xlabel("arb.u.")
plt.ylabel("Energy (eV)")
plt.show()