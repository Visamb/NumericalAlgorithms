"""Generic class for QuasiNewton"""
from numpy import *
from math import *
from linesearchmethods import*


class QuasiNewton:

    def __init__(self, problem):
        self.epsilon = 0.0001      # step size
        self.f = problem.function  # object function
        self.n = 2                 # the dimension of the domain, R^n
        self.alpha = 1             #
        self.values = array([])    #
        self.TOL = 1.e-8           #
        self.rho = 0.1
        self.sigma = 0.7
        self.tau = 0.1
        self.xi = 9

    def gradient(self, x):
        """
        Computes the gradient of f at the given point x by central-difference ((8.7) p.196 Nocedal, Wright)
        :return: (array)
        """
        g = empty((self.n, 1))
        for i in range(self.n):  # for every coordinate of x
            e = zeros((self.n, 1))  # unit vectors in the domain
            e[i] = self.epsilon  # we want to take a step in the i:th direction
            g[i] = (self.f(x + e) - self.f(x - e)) / (2 * self.epsilon)  # (8.1) at p.195
        return g

    def hessian(self, x):
        """
        Computes the inverse hessian of f at the given point x by forward-difference (p.201 Nocedal, Wright)
        :return: nxn matrix
        """
        G = empty((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                direction1 = zeros((self.n, 1))
                direction2 = zeros((self.n, 1))
                direction1[i] = self.epsilon
                direction2[j] = self.epsilon
                G[i, j] = (self.f(x + direction1 + direction2) - self.f(x + direction2) - self.f(
                    x + direction1) + self.f(x)) / (self.epsilon ** 2)
        G = (G + G.transpose()) / 2
        return G

    def newton_direction(self, x):
        """INTE ANVÄND ÄN. VET EJ OM VI KOMMER BEHÖVA DENNA SOM METOD"""
        inverse_hessian = linalg.inv(self.hessian(x))
        g = self.gradient(x)
        newton_direction = -inverse_hessian.dot(g)
        return newton_direction

        

    def newstep(self, x):
        """
        Computes coordinates for the next step in accordance with the Quasi Newton procedure.
        :return: (array)
        """

        inverse_hessian = linalg.inv(self.hessian(x))

        g = self.gradient(x)


        newton_direction = inverse_hessian.dot(g)  # The Newton direction determines step direction.


        new_coordinates = x - self.alpha*newton_direction
        return new_coordinates

    def newHessian(self):
        """Returns Hessian. Overridden in 9 special methods"""
        return

    def exactlinesearch(self, x):
        """
        Exact line search method as described in (3.3) p.31 Nocedal, Wright
        :param x:
        :return:
        """
        alphas = linspace(2, 0, 1000)
        min_alpha = alphas[1]
        direction = self.newton_direction(x)
        min_value = inf
        for alpha in alphas:
            current_value = self.f(x + alpha * direction)
            if current_value < min_value:
                min_alpha = alpha
                min_value = current_value


        return min_alpha

    def inexactlinesearch(self, f, x, alpha, s, rho, sigma, tau, xi):

        a_U = inf
        a_L = 0
        a_0 = alpha

        def f_alpha(alpha):
            fun = f(x + alpha * s)
            return fun

        def f_derivative(alpha):
            epsilon = 0.001
            fprime = (f(x + (alpha + epsilon) * s) - f(x + (alpha - epsilon) * s)) / (2 * epsilon)
            return fprime

        def leftcondition(alpha0, alphaL):
            if (f_derivative(alpha0) >= f_derivative(alphaL)):
                return True
            return False

        def rightcondition(alpha0, alphaL):
            if (f_alpha(alpha0) <= (f_alpha(alphaL) + rho * (alpha0 - alphaL) * f_derivative(alphaL))):
                return True
            return False

        while (any([leftcondition(a_0, a_L),rightcondition(a_0, a_L)] == False)):

               if (leftcondition(a_0, a_L) == False):
                delta = (a_0 - a_L) * ((f_derivative(a_0)) / (f_derivative(a_0) - f_derivative(a_L)))
                delta = max(delta, tau * (a_0 - a_L))
                delta = min(delta, xi * (a_0 - a_L))
                print("delta" + str(delta))
                a_L = a_0
                a_0 = a_0 + delta

               else:

                a_U = min(a_0, a_U)
                a0 = (((a_0 - a_L) ** 2) * f_derivative(a_L)) / (
                            2 * (f_alpha(a_L) - f_alpha(a_0) + (a_0 - a_L) * f_derivative(a_L)))
                a0 = max(a0, a_L + tau * (a_U - a_L))
                a0 = min(a0, a_U - tau * (a_U - a_L))
                print("delta" + str(a0))
                a_0 = a0


        return a_0


    def termination_criterion(self, x):
        """
        Asserts that the criterions for optimum are fulfilled. The criterions are:
        1.Hessian is symmetric and positive definite.
        2. The gradient is zero.
        :return: boolean that is true if criteria are fulfilled
        """
        Hess = self.hessian(x)
        if not all(self.gradient(x) < self.TOL):
            return False
        """
        else:
            try:
                linalg.cholesky(Hess)
            except:
                return False  # If the Choleskymethod gives error False is returned.
        """
        print("SOLVED!")
        return True

    def solve(self):
        x = ones((self.n, 1)) * 2
        self.alpha = inexact_linesearch(self.f,self.newton_direction(x),x,self.rho,self.sigma,self.tau,self.xi)

        solved = self.termination_criterion(x)
        value = x
        self.values = value
        while solved is False:
            self.alpha = inexact_linesearch(self.f, self.newton_direction(x), x, self.rho, self.sigma, self.tau, self.xi)
            newvalue = self.newstep(value)
            value = newvalue
            solved = self.termination_criterion(value)
            self.values = hstack([self.values, value])
        return [value, self.f(value)]
