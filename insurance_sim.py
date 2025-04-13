import numpy as np


import matplotlib.pyplot as plt
from tqdm import tqdm

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
        self.ammount_mc = ammount_mc # cantidad de iteraciones para monte carlo
        
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

        record = [] # almacenamos aqui datos de la sim por instante de tiempo t
        time_rate = self.v + n*self.mu + n*self.lam
        X = np.random.exponential(1/time_rate) # generamos X: tiempo hasta el prox evento
        t_E = X  # tiempo de espera
        ta = t # tiempo actual
        while True:
            record.append((t, n, a))
            
            # caso 1: terminamos?
            if t_E > self.T:
                return(1, t, record)
            # caso 2: procesar 
            elif t_E <= self.T:
                a += n*self.c*(t_E-t) # acumulamos pagos desde la iteracion anterior
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
                    a -= Y 
                    if a <= 0: 
                        record.append((t, n, a))
                        return (0, t, record) # valores negativos, perdimos mas dinero del que teniamos
            t_E = t + X     
                    
                

    # implementacion de monte carlo para estimar la probabilidad de no tener ingresos negativos
    def monte_carlo(self):
        results = []
        records = []
        still_have_money = 0

        for _ in tqdm(range(self.ammount_mc)):
            I, t, record = self.start_sim()
            results.append((I, t))
            records.append(record)
            still_have_money += I

        still_have_money_chance = still_have_money / self.ammount_mc
        average_time = np.mean([r[1] for r in results])

        return {
            'chance' :still_have_money_chance, 
            'records': records, 
            'average_time': average_time}

    # implementacion para visualizar resultados
    def visualize(self, records, example_num = 10):
        plt.figure(figsize=(12, 6))
        
        for i in range(min(example_num, len(records))):
            record = records[i]
            times = [r[0] for r in record]
            capital = [r[2] for r in record]
            
            # Determinar color según si hubo ruina
            color = 'green' if capital[-1] > 0 else 'red'
            plt.step(times, capital, where='post', 
                    alpha=0.5, color=color,
                    label=f'Ejecución {i+1}')
        
        plt.axhline(0, color='black', linestyle='--', label='Umbral de ruina')
        plt.xlabel('Tiempo')
        plt.ylabel('Capital de la compañía')
        plt.title('Trayectorias simuladas del capital')
        plt.legend()
        plt.grid(True)
        plt.show()

example_params = {
    'v' : 0.9,     # tasa de nuevos clientes 
    'mu': 0.1,     # tasa de abandono de clientes
    'lam': 0.1,   # tasa de reclamaciones por cliente
    'c': 10,       # pago de cliente por unidad de tiempo
    'a0': 50,        # capital inicial
    'n0': 5,         # cantidad inicial de clientes
    'T': 1000,       # tiempo maximo 
    'F': {   # distribucion de reclamaciones
        'mean': 0.5,
        'sigma': 0.8
    },
    'ammount_mc': 1000 # cantidad de iteraciones para monte carlo
}
if __name__ == "__main__":

    insurance_sim = InsuranceSim(
        example_params['v'],
        example_params['mu'],
        example_params['lam'],
        example_params['c'],
        example_params['a0'],
        example_params['n0'],
        example_params['T'],
        example_params['F'],
        example_params['ammount_mc'])
    
    results = insurance_sim.monte_carlo()
    
    print(f"\nResultados después de {example_params['ammount_mc']} simulaciones:")
    print(f"Probabilidad de no ruina: {results['chance']}")
    print(f"Tiempo promedio: {results['average_time']:.2f} unidades de tiempo")
    
    # visualizar algunas trayectorias
    #insurance_sim.visualize(results['records'])