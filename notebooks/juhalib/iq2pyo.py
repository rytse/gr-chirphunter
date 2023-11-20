import numpy as np
import sys

adj = np.fromfile(sys.argv[1], dtype=np.int16)
z = adj[0:len(adj)-1:2] + 1.0j * adj[1:len(adj):2]
z = z.astype(np.complex64)

np.save(sys.argv[2], z)
z.tofile(sys.argv[2])
