import lasio
import os
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 5})

class wellCleaner:
    """Cleans wells
    """
    
    # main args
    DT_UNIT = 1000000  # us
    Z_NMS = ["DEPT"]
    DT_NMS = ["DT"]
    RES_NMS = ["RESD"]
    GAM_NMS = ["GR"]
    
    # ricker args
    L_RICK = 0.256 #  s, half length
    F_RICK = 50 #  Hz
    DT_RICK = 0.001 #  s
    
    
    def __init__(self, las_file):
        self.NM = las_file.removesuffix('.las')
        self.las = lasio.read(las_file)
        print(self.las.curves)
        self.df = self.las.df().reset_index()
        self.__keep_cols()
            
        
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
        
        
    def write_las(self):
        DIR = "clean_las"
        self.df = self.df.set_index(self.df.columns[0])
        print(self.df)
        self.las.set_data(self.df)
        self.__set_headers()
        if not os.path.exists(DIR):
            os.mkdir(DIR)
        self.las.write(f"{DIR}/{self.NM}_clean.las")
        
        
    def __keep_cols(self):
        self.Z_NM = [x for x in self.df.columns if x in self.Z_NMS][0]
        self.DT_NM = [x for x in self.df.columns if x in self.DT_NMS][0]
        self.RES_NM = [x for x in self.df.columns if x in self.RES_NMS][0]
        self.GAM_NM = [x for x in self.df.columns if x in self.GAM_NMS][0]
       
        self.df = self.df[[self.Z_NM,
                           self.DT_NM,
                           self.RES_NM,
                           self.GAM_NM]]    
        
    def __set_headers(self):
        self.las.curves.V.unit = "ft/s"
        num = self.df.columns.get_loc("V")
        self.las.curves.V.descr = f"{num+2} VEL FROM DT"
        
        self.las.curves.AI.unit = "ohms"
        num = self.df.columns.get_loc("AI")
        self.las.curves.AI.descr = f"{num+2} IMPEDANCE"
        
        self.las.curves.RICK_QC.unit = "WAV"
        num = self.df.columns.get_loc("RICK_QC")
        self.las.curves.RICK_QC.descr = f"{num+2} RICKER WAVELET"
        
        self.las.curves.SYNT.unit = "SEIS"
        num = self.df.columns.get_loc("SYNT")
        self.las.curves.SYNT.descr = f"{num+2} SYNTHETIC TRACE"
        print(self.las.curves)

    def __v_from_dt(self, dt, z):
        return np.array(z) / np.array(dt) * self.DT_UNIT

    def __ai_from_v_rho(self, v, rho):
        return np.array(v) #   * np.array(rho)

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
               * np.exp(-(np.pi**2)*(self.F_RICK**2)*(t**2)))
        
        return wav

    def __rick_qc(self, z):
        rick = self.__make_ricker()
        return self.__resamp(rick, z)
    
    def __resamp(self, s, s_target):
        old_i = np.linspace(0, len(s_target)-1, num=len(s))
        new_i = np.linspace(0, len(s_target)-1, num=len(s_target))

        return np.interp(new_i, old_i, s)
    