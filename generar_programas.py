import os
import random
from configuration import *

nargo_toml = '''[package]
name = "ejemplo"
type = "bin"
authors = [""]
compiler_version = ">=0.31.0"

[dependencies]'''

def generar_n(name, n_values, input_generator):
    with open(f'./templates/{name}.nr', 'r') as template_file:
        template = template_file.read()
        for n in n_values:
            instance_n = template.replace('N', str(n))
            os.makedirs(f'./programas_generados/{name}/{n}', exist_ok=True)
            os.makedirs(f'./programas_generados/{name}/{n}/src', exist_ok=True)
            with open(f'./programas_generados/{name}/{n}/Nargo.toml', 'w') as manifest:
                manifest.write(nargo_toml)
            with open(f'./programas_generados/{name}/{n}/Prover.toml', 'w') as inputs:
                inputs.write(input_generator(n))
            with open(f'./programas_generados/{name}/{n}/src/main.nr', 'w') as instance_file_n:
                instance_file_n.write(instance_n)

def generar_n_k(name, n_values, input_generator):
    with open(f'./templates/{name}.nr', 'r') as template_file:
        template = template_file.read()
        for k in [8,16,32]:
            for n in n_values:
                instance = template.replace('N', str(n))
                instance = instance.replace('K', str(k))
                os.makedirs(f'./programas_generados/{name}/u{k}/{n}', exist_ok=True)
                os.makedirs(f'./programas_generados/{name}/u{k}/{n}/src', exist_ok=True)
                with open(f'./programas_generados/{name}/u{k}/{n}/Nargo.toml', 'w') as manifest:
                    manifest.write(nargo_toml)
                with open(f'./programas_generados/{name}/u{k}/{n}/Prover.toml', 'w') as inputs:
                    inputs.write(input_generator(k,n))
                with open(f'./programas_generados/{name}/u{k}/{n}/src/main.nr', 'w') as instance_file:
                    instance_file.write(instance)


def input_for_assert_zero(n):
    random_inputs = [random.randint(0, 2**32) for _ in range(n)]
    return f'a = {str(random_inputs)}'

def input_for_memory(_):
    return '''idx = 0
val = 0'''

def input_for_range(k,n):
    random_inputs = [random.randint(0, (2**k)-1) for _ in range(n)]
    return f'a = {str(random_inputs)}'

def input_for_xor(k,_):
    random_input_a = random.randint(0, (2**k)-1)
    random_input_b = random.randint(0, (2**k)-1)
    return f'''a = {random_input_a}
b = {random_input_b}'''

def generar_programas():
    generar_n("assert_zero", sizes_per_program_family["assert_zero"], input_for_assert_zero)
    generar_n("memory", sizes_per_program_family["memory"], input_for_memory)
    generar_n("memory_wide", sizes_per_program_family["memory_wide"], input_for_memory)
    generar_n_k("range", sizes_per_program_family["range/u8"], input_for_range)
    generar_n_k("xor", sizes_per_program_family["xor/u8"], input_for_xor)

if __name__ == "__main__":
    #generar_programas()
    generar_n_k("range", [50000, 100000], input_for_range)

