'''
inventoryanalytics: a Python library for Inventory Analytics

Author: Roberto Rossi

MIT License
  
Copyright (c) 2018 Roberto Rossi
'''

from scipy.optimize import minimize
import matplotlib.pyplot as plt

class eoq:
    '''
    Ford W. Harris, How Many Parts to Make at Once, Factory, 
    The Magazine of Management, Volume 10, Number 2, February 1913, pp. 135–136, 152.

    Harris, Ford W. (1990). "How Many Parts to Make at Once". Operations Research. 
    38 (6): 947. doi:10.1287/opre.38.6.947.
    '''

    def __init__(self, K: float, h: float, d: float, v: float):
        """
        Constructs an instance of the Economic Order Quantity problem.
        
        Arguments:
            K {float} -- the fixed ordering cost
            h {float} -- the proportional holding cost
            d {float} -- the demand per period
            v {float} -- the unit purchasing cost
        """

        self.K, self.h, self.d, self.v = K, h, d, v

    def compute_eoq(self) -> float:
        """
        Computes the Economic Order Quantity.
        
        Returns:
            float -- the Economic Order Quantity
        """

        x0 = 1 # start from a positive EOQ
        res = minimize(self.relevant_cost, x0, method='nelder-mead', 
                       options={'xtol': 1e-8, 'disp': False})
        return res.x[0]

    def relevant_cost(self, Q: float) -> float:
        """
        Computes the relevant cost (ignoring the unit production cost) 
        per unit period for a given quantity Q.
        
        Arguments:
            Q {float} -- the order quantity

        Returns:
            float -- the optimal cost per unit period
        """

        return self.co_fixed(Q)+self.ch(Q)

    def cost(self, Q: float) -> float:
        """
        Computes the total cost per unit period for a given quantity Q.
        
        Arguments:
            Q {float} -- the order quantity

        Returns:
            float -- the optimal cost per unit period
        """

        return self.co_fixed(Q)+self.co_variable(Q)+self.ch(Q)

    def co_fixed(self, Q: float) -> float:
        """
        Computes the fixed ordering cost
        
        Arguments:
            Q {float} -- the order quantity
        
        Returns:
            float -- the fixed ordering cost
        """

        K, d= self.K, self.d
        return K/(Q/d)

    def co_variable(self, Q: float) -> float:
        """
        Computes the variable ordering cost
        
        Arguments:
            Q {float} -- the order quantity
        
        Returns:
            float -- the variable ordering cost
        """        
        d, v = self.d, self.v
        return d*v

    def ch(self, Q: float) -> float:
        """
        Computes the inventory holding cost
        
        Arguments:
            Q {float} -- the order quantity
        
        Returns:
            float -- the inventory holding cost
        """
        h = self.h
        return h*Q/2

    def coverage(self) -> float:
        """
        Compute the number of periods of demand the 
        Economic Order Quantity will satisfy.
        
        Returns:
            float -- the number of periods of demand the 
                Economic Order Quantity will satisfy
        """

        d = self.d
        return self.compute_eoq()/d

    def average_inventory(self) -> float:
        """
        Computes the average inventory level 
        
        Returns:
            float -- the average inventory level 
        """

        return self.compute_eoq()/2

    def itr(self) -> float:
        """
        The Implied Turnover Ratio (ITR) represents the number of times 
        inventory is sold or used in a time period.
        
        Returns:
            float -- the Implied Turnover Ratio (ITR)
        """

        d = self.d
        return 2*d/self.compute_eoq()

    def sensitivity_to_Q(self, Q: float) -> float:
        """
        Computes the additional cost faced if the 
        chosen order quantity `Q` deviates from the 
        optimal order quantity.
        
        Arguments:
            Q {float} -- the target order quantity
        
        Returns:
            float -- a ratio indicating the percent 
                increase, e.g. 1.05 is a 5% increase
        """
        Qopt = self.compute_eoq()
        return 0.5*(Qopt/Q+Q/Qopt)

    def reorder_point(self, lead_time: float) -> float:
        """
        Computes the reorder point for a given lead time.
        
        Arguments:
            lead_time {float} -- the given lead time
        
        Returns:
            float -- the reorder point
        """

        d = self.d
        return d*lead_time

    @staticmethod
    def _plot_eoq():
        instance = {"K": 100, "h": 1, "d": 10, "v": 2}
        pb = eoq(**instance)
        total, = plt.plot([k for k in range(10,100)], 
                          [pb.relevant_cost(k) for k in range(10,100)], 
                          label='Total relevant cost')
        ordering, = plt.plot([k for k in range(10,100)], 
                             [pb.co_fixed(k) for k in range(10,100)], 
                             label='Ordering cost')
        holding, = plt.plot([k for k in range(10,100)], 
                            [pb.ch(k) for k in range(10,100)], 
                            label='Holding cost')
        plt.legend(handles=[total,ordering,holding], loc=1)
        plt.ylabel('Cost')
        plt.xlabel('Q')
        plt.show()
    
    @staticmethod
    def _plot_sensitivity_to_Q():
        instance = {"K": 100, "h": 1, "d": 10, "v": 2}
        pb = eoq(**instance)
        plt.plot([k for k in range(20,80)], [pb.sensitivity_to_Q(k) for k in range(20,80)])
        plt.ylabel('Sensitivity')
        plt.xlabel('Q')
        plt.show() 

    @staticmethod
    def _sample_instance():
        instance = {"K": 100, "h": 1, "d": 10, "v": 2}
        pb = eoq(**instance)
        Qopt = pb.compute_eoq()
        print(Qopt)
        print(pb.relevant_cost(Qopt))

if __name__ == '__main__':
    #eoq._plot_eoq()
    eoq._plot_sensitivity_to_Q()
    #eoq._sample_instance()

