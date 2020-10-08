from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.rank  # rank of current process
size = comm.size  # number of working processes

#Gamma2 gets outer border from Gamma1 and Gamma3
# Gamma1 and Gamma3 gets inner border from Gamma2
#Gamma2 gets new outer border from Gamma1 and Gamma3
#...

#UNC is Vi+1-vi-1/h vi+1 = inner border


