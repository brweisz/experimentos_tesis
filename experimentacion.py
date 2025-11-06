# In[ ]:
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess
import os
import time
import configuration
from datetime import datetime

# In[ ]:
BASE_PATH = os.getcwd()
NARGO_NOIRKY2_PATH = BASE_PATH + "/nargo_versions/nargo_noirky2"
NARGO_BARRETENBERG_PATH = BASE_PATH + "/nargo_versions/nargo_barretenberg"

# In[ ]:
def nargo_build(program_path, executable_path, witness_name, binary_name):
    os.chdir(BASE_PATH+f"/programas_generados/{program_path}")
    subprocess.run([executable_path, "execute", witness_name])
    subprocess.run(["mv", "target/ejemplo.json", f"target/{binary_name}.json"])
    os.chdir(BASE_PATH)
        
def nargo_build_all(executable_path, witness_name, binary_name):
    for program in configuration.sizes_per_program_family.keys():
        for n in configuration.sizes_per_program_family[program]:
            nargo_build(f"{program}/{n}/", executable_path, witness_name, binary_name)

def nargo_noirky2_build_all():
    nargo_build_all(NARGO_NOIRKY2_PATH, "witness_noirky2", "binary_noirky2")

def nargo_barretenberg_build_all():
    nargo_build_all(NARGO_BARRETENBERG_PATH, "witness_bb", "binary_bb")

# In[ ]:
# Nos aseguramos que el ACIR sea el mismo para ambas versiones
#for program in configuration.program_families:
#    for n in configuration.sizes_per_program_family[program]:
#        os.chdir(BASE_PATH + f"/programas_generados/{program}/{n}")
#        out_noirky2 = subprocess.run([NARGO_NOIRKY2_PATH, "build", "--print-acir"], capture_output=True)
#        out_barretenberg = subprocess.run([NARGO_BARRETENBERG_PATH, "build", "--print-acir"], capture_output=True)
#        assert out_noirky2.stdout == out_barretenberg.stdout
#        os.chdir(BASE_PATH)

# In[ ]:
#nargo_barretenberg_build_all()

# In[ ]:
#nargo_noirky2_build_all()

# In[ ]:
def prove(path_to_backend, path_to_program, path_to_witness, path_to_proof, path_to_binary):
    os.chdir(BASE_PATH+f"/programas_generados/{path_to_program}")
    start_time = time.time()
    subprocess.run([path_to_backend, "prove", "-b", path_to_binary, "-w", path_to_witness, "-o", path_to_proof])
    end_time = time.time()
    os.chdir(BASE_PATH)
    return end_time - start_time

# In[ ]:
def write_vk(path_to_backend, path_to_program, path_to_vk, path_to_binary):
    os.chdir(BASE_PATH+f"/programas_generados/{path_to_program}")
    start_time = time.time()
    subprocess.run([path_to_backend, "write_vk", "-b", path_to_binary, "-o", path_to_vk])
    end_time = time.time()
    os.chdir(BASE_PATH)
    return end_time - start_time

# In[ ]:
def verify(path_to_backend, path_to_program, path_to_vk, path_to_proof):
    os.chdir(BASE_PATH+f"/programas_generados/{path_to_program}")
    start_time = time.time()
    subprocess.run([path_to_backend, "verify", "-k", path_to_vk, "-p", path_to_proof])
    end_time = time.time()
    os.chdir(BASE_PATH)
    return end_time - start_time

# In[ ]:
comandos = ["prove", "write_vk", "verify"]
ejemplos = configuration.program_families
cantidad_de_iteraciones = 20
timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

# In[ ]:
backend_base = {
    "noirky2-bits": "noirky2",
    "noirky2-bits-nozk": "noirky2",
    "noirky2-limb": "noirky2",
    "noirky2-limb-nozk": "noirky2",
    "bb": "bb"
}

temp_csv_name = f"mediciones/incremental_{timestamp}.csv"

rows = []
local_rows = []

for comando in comandos:
    for ejemplo in configuration.sizes_per_program_family.keys():
        for backend in configuration.backends_per_program_family[ejemplo]:
            for n in configuration.sizes_per_program_family[ejemplo]:
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
                    elif comando == "verify":
                        time_elapsed = verify(
                            f"{BASE_PATH}/backends/{backend}",
                            f"{ejemplo}/{n}",
                            f"target/vk_{backend}",
                            f"target/proof_{backend}")
                    else:
                        print("----------COMANDO DESCONOCIDO------------")
                        pass
                        
                    muestra = {"comando": comando, "backend": backend, "ejemplo": ejemplo, "n": n, "iteracion": m, "tiempo": time_elapsed}
                    print(muestra)
                    rows.append(muestra)
                    local_rows.append(muestra)
                df = pd.DataFrame(local_rows)
                df.to_csv(temp_csv_name, mode="a", header=not os.path.exists(temp_csv_name), index=False)
                local_rows = []  

muestra_headers = ["comando", "backend", "ejemplo", "n", "iteracion", "tiempo"]
df_tiempos = pd.DataFrame(rows, columns = muestra_headers)
df_tiempos

# In[ ]:
timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
filename = f"tiempos_{timestamp}.csv"
df_tiempos.to_csv(f"mediciones/{filename}", index=False)

# In[ ]:
#df_tiempos = pd.read_csv("mediciones/mediciones.csv")

# In[ ]:
# ----------- GRAFICOS DE TIEMPOS  ------------ #
cols = 3
rows = 3

for comando in comandos:
    fig, axes = plt.subplots(rows, cols, figsize=(12, 5 * rows))
    axes = axes.flatten()
    
    for idx, ejemplo in enumerate(ejemplos):
        subset = df_tiempos[(df_tiempos["ejemplo"] == ejemplo) & (df_tiempos["comando"] == comando)]
        sns.lineplot(data=subset, x="n", y="tiempo", hue="backend", ax=axes[idx])
        axes[idx].set_title(f"{comando}-{ejemplo}")
        axes[idx].set_xlabel("n")
        axes[idx].set_ylabel("tiempo")
    
    # Hide any unused subplots
    for j in range(len(ejemplos), len(axes)):
        fig.delaxes(axes[j])
    
    plt.tight_layout()
    plt.savefig(f"mediciones/{comando}_tiempos_{timestamp}.png")
    plt.show()

# In[ ]:
# OBTENER TAMAÑOS
command_to_artifact = {"prove": "proof", "write_vk": "vk"}
def get_size_in_bytes(comando, backend, ejemplo, n):
    artifact_name = command_to_artifact[comando]
    file_path = f"{BASE_PATH}/programas_generados/{ejemplo}/{n}/target/{artifact_name}_{backend}"
    byte_size = os.path.getsize(file_path)
    print(file_path)
    print(byte_size)
    return byte_size

rows = []

for comando in ["prove", "write_vk"]:
    for ejemplo in ejemplos:
        for backend in configuration.backends_per_program_family[ejemplo]:
            for n in configuration.sizes_per_program_family[ejemplo]:
                byte_size = get_size_in_bytes(comando, backend, ejemplo, n)
                rows.append({"comando": comando, "backend": backend, "ejemplo": ejemplo, "n": n, "byte_size": byte_size})

columns = ["comando", "backend", "ejemplo", "n", "byte_size"]
df_sizes = pd.DataFrame(rows, columns = columns)
df_sizes

# In[ ]:
# ---------- GRAFICOS DE TAMAÑOS ---------- #
cols = 3
rows = 3

for comando in ["prove", "write_vk"]:
    fig, axes = plt.subplots(rows, cols, figsize=(12, 5 * rows))
    axes = axes.flatten()

    for idx, ejemplo in enumerate(ejemplos):
        subset = df_sizes[(df_sizes["ejemplo"] == ejemplo) & (df_sizes["comando"] == comando)]
        sns.barplot(data=subset, x="n", y="byte_size", hue="backend", ax=axes[idx])
        axes[idx].set_title(f"{comando}-{ejemplo}")
        axes[idx].set_xlabel("n")
        axes[idx].set_ylabel("byte_size")

    # Hide any unused subplots
    for j in range(len(ejemplos), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.savefig(f"mediciones/{comando}_tamanios_{timestamp}.png")
    plt.show()

# In[ ]:


