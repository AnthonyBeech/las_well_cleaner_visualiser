import lasio
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 5})

class wellCleaner:
    """Cleans wells
    """
    
    # main args
    DT_UNIT = 1000000  # us
    Z_NM = "DEPT"
    DT_NM = "DT"
    RES_NM = "RESD"
    
    # ricker args
    L_RICK = 0.256 # ms, half length
    F_RICK = 50 #12 # Hz
    DT_RICK = 0.001
    
    
    def __init__(self, las_file):
        self.las = lasio.read(FLOC)
        print(self.las.curves)
        self.df = self.las.df().reset_index()
        
        
    def clean(self):
        self.df["V"] = self.__v_from_dt(self.df[self.Z_NM], self.df[self.DT_NM])
        self.df["AI"] = self.__ai_from_v_rho(self.df["V"], self.df[self.RES_NM])
        self.df["RICK_QC"] = self.__rick_qc(self.df[self.Z_NM])
        self.df["SYNT"] = self.__make_synt(self.df["AI"])
        
    
    def print_logs(self):
        z = self.df["DEPT"]
        df = self.df.drop(columns="DEPT")
        N = len(df.columns)
        
        fig, ax = plt.subplots(1, N)
        for i, _log in enumerate(df):
            ax[i].plot(df[_log], z)
            ax[i].set_title(_log)
        
        plt.tight_layout()
        plt.show()


    def __v_from_dt(self, dt, z):
        return np.array(z) / np.array(dt) * self.DT_UNIT

    def __ai_from_v_rho(self, v, rho):
        return np.array(v) * np.array(rho)

    def __make_synt(self, ai):
        ref = np.diff(ai)
        ref = np.insert(ref, 0, 0, axis=0)

        synt = np.convolve(ref, self.__make_ricker(), mode='same')
        
        return self.__resamp(synt, ref)
    
    def __make_ricker(self):    
        first = -1 * self.L_RICK / 2
        last = (self.L_RICK - self.DT_RICK) / 2
        
        t = np.arange(first, last, self.DT_RICK)
        
        # formula for ricker wavelet
        wav = ((1.0 - 2.0*(np.pi**2)*(self.F_RICK**2)*(t**2)) 
               * np.exp(-(np.pi**2)*(self.F_RICK**2))*(t**2))
        
        return wav

    def __rick_qc(self, z):
        rick = self.__make_ricker()
        return self.__resamp(rick, z)
    
    def __resamp(s, s_target):
        old_i = np.linspace(0, len(s_target)-1, num=len(s))
        new_i = np.linspace(0, len(s_target)-1, num=len(s_target))

        return np.interp(new_i, old_i, s)


FLOC = "test_well.las"

wells = wellCleaner(FLOC)
wells.clean()
wells.print_logs()
