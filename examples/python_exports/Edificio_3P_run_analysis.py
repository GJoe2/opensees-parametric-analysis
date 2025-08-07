from Edificio_3P_model import build_model
import openseespy.opensees as ops
import numpy as np


def run_analysis():
    print('\n--- Iniciando Análisis Estático ---')
    try:
        ops.system('BandGeneral')
        ops.numberer('RCM')
        ops.constraints('Plain')
        ops.integrator('LoadControl', 1.0 / 20)
        ops.algorithm('Linear')
        ops.analysis('Static')
        ops.analyze(20)
        print('Análisis estático completado exitosamente.')
    except Exception as e:
        print(f'Error en análisis estático: {e}')

    print('\n--- Iniciando Análisis Modal ---')
    try:
        ops.setTime(0.0)
        ops.remove('loadPattern', 1)

        num_modes = 10
        eigen_values = ops.eigen(num_modes)
        print('Períodos Modales (s):')
        for i, val in enumerate(eigen_values):
            if val > 1e-6:
                freq = np.sqrt(val) / (2 * np.pi)
                period = 1.0 / freq
                print(f'  - Modo {i+1}: {period:.4f} s')
        print('Análisis modal completado exitosamente.')
    except Exception as e:
        print(f'Error en análisis modal: {e}')


if __name__ == '__main__':
    build_model()
    print('Modelo construido exitosamente.')
    run_analysis()