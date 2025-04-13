import numpy as np
import matplotlib as plt

class InsuranceSim:
    def __init__(self, v, mu, lam, c, a0, n0, t, F, ammount_mc):
        self.v = v # tasa de nuevos clientes
        self.mu = mu # tasa de abandono de clientes
        self.lam = lam # tasa de reclamaciones por cliente
        self.c = c # pago de cliente por unidad de tiempo
        self.a0 = a0 # capital inicial
        self.n0 = n0 # cantidad inicial de clientes
        self.t = t # tiempo
        self.F = F # distribucion de reclamaciones
        self.ammount_mc = ammount_mc # cantidad de iteraciones de monte carlo
    
    def start_sim(self):
        pass

    def monte_carlo(self):
        pass

    def visualize(self):
        pass