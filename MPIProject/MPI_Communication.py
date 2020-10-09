from mpi4py import MPI
from heat_transfer import *
from Domain_One import*
from Domain_Two import*
from Domain_Three import*

class MPI_heat_transfer:

        comm = MPI.COMM_WORLD
        rank = comm.rank  # rank of current process
        size = comm.size  # number of working processes


        #Initializing domains for storing temperatures.
        Domain_One = Domain_One()
        Domain_Two = Domain_Two()
        Domain_Three = Domain_Three()

        border1 = Domain_One.compute_distribution(None)
        border2 = Domain_Three.compute_distribution(None)

        k = 1
        t = 1
        s = 1

        while k < 4 and s < 4 and t < 4:

                if rank == 0:
                    if k == 1:
                        border = Domain_One.compute_distribution(None)
                        comm.send(border, dest=1)
                        s += 1
                    else:
                        gamma = comm.recv(source = 1)
                        border = Domain_One.compute_distribution(gamma)
                        comm.send(border,dest=1)
                        s += 1
                        print(s)
                        print(border)
                if rank == 1 and s == t:

                        border1 = comm.recv(source=0)
                        border2 = comm.recv(source=2)
                        #print(border1,border2)
                        gamma1,gamma2 = Domain_Two.compute_distribution(border1,border2)
                        k+=1
                        print("COUNTING")
                        print(k)
                        #print(s)
                        comm.send(gamma1, dest=0)
                        comm.send(gamma2, dest=2)

                if rank == 2:
                    if k == 1:
                        border = Domain_Three.compute_distribution(None)
                        comm.send(border, dest=1)
                        t += 1
                    else:
                        gamma = comm.recv(source=1)
                        border = Domain_Three.compute_distribution(gamma)
                        comm.send(border, dest=1)
                        t += 1

        print(Domain_One.T_domain_one)
        print()
        print(Domain_Two.T_domain_two)
        print()
        print(Domain_Three.T_domain_three)



