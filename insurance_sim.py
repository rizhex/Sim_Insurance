import numpy as np
import matplotlib as plt

class InsuranceSim:
    def __init__(self, v, mu, lam, c, a0, n0, T, F, ammount_mc):
        self.v = v # tasa de nuevos clientes
        self.mu = mu # tasa de abandono de clientes
        self.lam = lam # tasa de reclamaciones por cliente
        self.c = c # pago de cliente por unidad de tiempo
        self.a0 = a0 # capital inicial
        self.n0 = n0 # cantidad inicial de clientes
        self.T = T # tiempo maximo 
        self.F = F # distribucion de reclamaciones
        self.ammount_mc = ammount_mc # cantidad de iteraciones de monte carlo
        
        # distribucion de las reclamaciones
        self.claim_dist = lambda: np.random.lognormal(
            mean = self.F['mean'],
            sigma = self.F['sigma']
        )

    def start_sim(self):
        # inicializamos las variables para una ejecucion de la simulacion
        t = 0
        a = self.a0
        n = self.n0

        record = [(t, n, a)] # almacenamos aqui datos de la sim por instante de tiempo t

        total_rate = self.v + n*self.mu + n*self.lam
        X = np.random.exponential(1/total_rate) # generamos X: tiempo hasta el prox evento
        t_E = X

        while True:
            # caso 1: terminamos?
            if t_E > self.T:
                return(1, t_E, record)
            # caso 2: procesar 
            elif t_E <= self.T:
                
                a += n*self.c * (t_E - t) # acumulamos pagos desde la iteracion anterior
                t = t_E

                # determinamos cual sera el siguiente evento J
                ev_p = np.array([self.v, n*self.mu, n*self.lam])
                ev_p = ev_p / ev_p.sum()
                J = np.random.choice([1, 2, 3], p = ev_p)

                if J == 1: n+=1 # cliente nuevo
                elif J == 2: # perdida de cliente
                    if n > 0: n-=1
                else: # reclamacion de un cliente
                    Y = self.claim_dist()
                    if Y > a:  # valores negativos, perdimos mas dinero del que teniamos
                        return (0, t, record)
                    a -= Y



    def monte_carlo(self):
        pass

    def visualize(self):
        pass