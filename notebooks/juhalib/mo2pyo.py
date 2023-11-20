import numpy as np
import sys

adj = np.fromfile(sys.argv[1], dtype=np.dtype('d'))
z = adj[0:int(len(adj) /2)] + 1.0j * adj[int(len(adj)/2):]
z = z.astype(np.complex64)

np.save(sys.argv[2], z)
z.tofile(sys.argv[2])
