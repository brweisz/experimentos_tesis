import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess
import os
import time
import configuration
from datetime import datetime
import numpy as np

BASE_PATH = os.getcwd()
NARGO_NOIRKY2_PATH = BASE_PATH + "/nargo_versions/nargo_noirky2"
NARGO_BARRETENBERG_PATH = BASE_PATH + "/nargo_versions/nargo_barretenberg"

def prove(path_to_backend, path_to_program, path_to_witness, path_to_proof, path_to_binary):
    os.chdir(BASE_PATH+f"/programas_generados/{path_to_program}")
    start_time = time.time()
    subprocess.run([path_to_backend, "prove", "-b", path_to_binary, "-w", path_to_witness, "-o", path_to_proof])
    end_time = time.time()
    os.chdir(BASE_PATH)
    return end_time - start_time

def write_vk(path_to_backend, path_to_program, path_to_vk, path_to_binary):
    os.chdir(BASE_PATH+f"/programas_generados/{path_to_program}")
    start_time = time.time()
    subprocess.run([path_to_backend, "write_vk", "-b", path_to_binary, "-o", path_to_vk])
    end_time = time.time()
    os.chdir(BASE_PATH)
    return end_time - start_time

comandos = ["prove", "write_vk"]
ejemplos = configuration.program_families
cantidad_de_iteraciones = 20

backend_base = {
    "noirky2-bits": "noirky2",
    "noirky2-bits-nozk": "noirky2",
    "noirky2-limb": "noirky2",
    "noirky2-limb-nozk": "noirky2",
    "bb": "bb"
}

rows = []
local_rows = []

for comando in comandos:
    for ejemplo in ["range/u8", "range/u16", "range/u32"]: #configuration.sizes_per_program_family.keys():
        for backend in configuration.backends_per_program_family[ejemplo]:
            for n in [1000, 2000, 5000, 10000, 20000, 50000, 100000]:
                for m in range(cantidad_de_iteraciones):
                    time_elapsed = 0
                    backend_base_name = backend_base[backend]
                    if comando == "prove":
                        time_elapsed = prove(
                            f"{BASE_PATH}/backends/{backend}",
                            f"{ejemplo}/{n}",
                            f"target/witness_{backend_base_name}.gz",
                            f"target/proof_{backend}",
                            f"target/binary_{backend_base_name}.json")
                    elif comando == "write_vk":
                        time_elapsed = write_vk(
                            f"{BASE_PATH}/backends/{backend}",
                            f"{ejemplo}/{n}",
                            f"target/vk_{backend}",
                            f"target/binary_{backend_base_name}.json")
                    else:
                        print("----------COMANDO DESCONOCIDO------------")
                        pass

                    muestra = {"comando": comando, "backend": backend, "ejemplo": ejemplo, "n": n, "iteracion": m, "tiempo": time_elapsed}
                    print(muestra)
                    rows.append(muestra)

muestra_headers = ["comando", "backend", "ejemplo", "n", "iteracion", "tiempo"]
df_tiempos = pd.DataFrame(rows, columns = muestra_headers)
timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
filename = f"tiempos_range_repetidos_{timestamp}.csv"
df_tiempos.to_csv(f"mediciones/{filename}", index=False)