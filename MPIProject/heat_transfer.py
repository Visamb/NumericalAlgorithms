

#Area 2 sends boundary temperature to Area 1
#The heat equation is solved in Area 1 with the temperature as a Dirichlet condition
#The solution is used to calculate the Neumann condition at the boundary, which is sent to Area 2
# The heat equation is solved in area 2 with Neumann condition
# RELAX


from scipy import sparse
import numpy as np

#DOMAIN2





# row indices
rowind = np.array([0, 0, 1, 1, 1, 2, 2, 2, 3, 3])

# column indices
colind = np.array([0, 1, 0, 1, 2, 1, 2, 3, 2, 3])

# matrix values
values = np.array([-2.,1.,1.,-2.,1.,1.,-2.,1.,1.,-2.])

# create sparse from COO format
# all arrays have the same length
A = sparse.csr_matrix( (values, (rowind, colind) ) )

# let's see what we got
print (A)

U_N = 15
U_H = 40
U_W = 5






