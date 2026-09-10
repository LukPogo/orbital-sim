import h5py
import numpy as np


def initialize_h5_file(file_name: str) -> None:
    with h5py.File(file_name, "w"):
        pass


# Aktualnie funkcja działa w taki sposób, że do konkretnej nazwy pliku ląduje czas i trajektoria
# Jest to zatem bardzo dedykowana wersja zapisu do tego konkretnego przypadku
def h5_save_time_traj(
    h5_file_name: str, group_name: str, time: np.ndarray, trajectory: np.ndarray
) -> None:
    with h5py.File(h5_file_name, "a") as f:
        grupa = f.create_group(group_name)
        grupa.create_dataset("trajectory", data=trajectory)
        grupa.create_dataset("time", data=time)


# Funkcja, której zadaniem jest odzyskać trajektorię i czas, w tej samej kolejności
# Być może obie nazwy brzmią zbyt ogólnie do swojego celu
# Może da się to napisać lepiej, korzystając z możliwości h5py
def h5_load_time_traj(
    h5_file_name: str, group_name: str
) -> tuple[np.ndarray, np.ndarray]:
    with h5py.File(h5_file_name, "r") as f:
        grupa = f[group_name]
        trajectory = grupa["trajectory"][:]
        time = grupa["time"][:]
    return time, trajectory
