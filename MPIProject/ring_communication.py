from mpi4py import MPI

"""
Sum the ranks of each process by letting the processes 
communicate as in a 1d torus
"""

comm = MPI.COMM_WORLD
rank = comm.rank  # rank of current process
size = comm.size  # number of working processes

if rank == 0:
    print("We are working on {} processes".format(size))
    #Sends rank 0 to rank 1
    comm.send(rank, dest=1)

    s = comm.recv(source=size-1)
    #Prints what was recieved from rank 3.
    print("Sum of ranks is {}".format(s))
else:
    #Rank 1 receives from 0 and sends 1 to 2%4 = 4
    #Rank 2 receives from 1 and sends 1+2 to 3%4 = 3
    #Rank 3 receives from 2 and sends 3+3 to 4%4 = 0
    received = comm.recv(source=rank-1)
    comm.send(received + rank, dest=(rank+1) % size)


""" FACIT
s = comm.allreduce(rank, op=MPI.SUM)
if rank == 0:
    print(s)"""