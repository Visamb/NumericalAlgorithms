# This is a sample Python script.

# Press Skift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from mpi4py import MPI
import numpy as np
from scipy import*
from scipy.sparse import diags
from heat_transfer import *
import matplotlib.pyplot as plt

comm = MPI.COMM_WORLD
print("Hello World: process ", comm.Get_rank(), " out of ", comm.Get_size(), " is reporting for duty!")


h = heat_transfer()
print(h.T_domain_one)
print(h.T_domain_two)
print(h.T_domain_three)

print()
print("INITIALIZING")

h.compute_distribution(domain = 1)
print(h.T_domain_one)
print()

k = 1

while k < 10:
    print("NEW COMPUTATION")
    h.compute_distribution(domain = 2)
    h.compute_distribution(domain = 1)
    h.compute_distribution(domain = 3)
    k+=1
print(h.T_domain_one)
print()
print(h.T_domain_two)
print()
print(h.T_domain_three)
print()
nx = h.n
ny = 2*nx
x = linspace(0, 1, nx + 2)
y = linspace(0, 2, ny + 2)
X, Y = meshgrid(x, y)

T = h.T_domain_two

h = plt.contourf(X, Y, T)
plt.colorbar(aspect=4)
plt.show()













