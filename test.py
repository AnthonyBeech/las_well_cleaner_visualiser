import lasio
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 5})


def v_from_dt(dt_log, z_log):
    """
    """
    
    N = len(dt_log)
    v = [0] * N
    
    for i in range(N):
        v[i] = z_log[i] / dt_log[i] * 1000000
        
    
    return v


def ai_from_v_rho(v, rho):
    """
    """
    
    N = len(v)
    ai = [0]*N
    
    for i in range(N):
        ai[i] = v[i] * rho[i]
        
    return v # ai


def make_synt(ai):
    """
    """
    reflectivity = np.diff(ai)
    reflectivity = np.insert(reflectivity, 0, 0, axis=0)
    
    print(len(reflectivity))
    synthetic_seismogram = np.convolve(reflectivity, make_ricker(), mode='same')
    print(len(synthetic_seismogram))
    
    old_indices = np.linspace(0, len(reflectivity)-1, num=len(reflectivity))
    new_indices = np.linspace(0, len(reflectivity)-1, num=len(synthetic_seismogram))

    resampled_signal = np.interp(old_indices, new_indices, synthetic_seismogram)
    
    return resampled_signal


def rick_qc(z):
    """
    """
    L = len(z)
    rick = make_ricker()
    old_indices = np.linspace(0, len(rick)-1, num=len(rick))
    new_indices = np.linspace(0, len(rick)-1, num=L)

    resampled_signal = np.interp(new_indices, old_indices, rick)
    
    return resampled_signal


def make_ricker():
    """
    """
    L = 0.256 # ms, half length
    pi = np.pi
    f = 50 #12 # Hz
    dt = 0.001
    
    t = np.arange(-L / 2, (L-dt) / 2, dt)
    print(t)
    y = (1.0 - 2.0*(np.pi**2)*(f**2)*(t**2)) * np.exp(-(np.pi**2)*(f**2)*(t**2))
    
    return y


def print_logs(df):
    """
    """
    z = df["DEPT"]
    df = df.drop(columns="DEPT")
    N = len(df.columns)
    
    fig, ax = plt.subplots(1, N)
    for i, _log in enumerate(df):
        ax[i].plot(df[_log], z)
        ax[i].set_title(_log)
        
    plt.show()

    return 0


FLOC = "test_well.las"
las = lasio.read(FLOC)
print(las.curves)

make_ricker()

df = las.df().reset_index()

df["V"] = v_from_dt(df["DEPT"], df["DT"])
df["AI"] = ai_from_v_rho(df["V"], df["RESD"])
df["RICK_QC"] = rick_qc(df["DEPT"])
df["SYNT"] = make_synt(df["AI"])

print_logs(df)
