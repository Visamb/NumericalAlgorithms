# This is a sample Python script.

# Press Skift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
print("Hello World: process ", comm.Get_rank(), " out of ", comm.Get_size(), " is reporting for duty!")