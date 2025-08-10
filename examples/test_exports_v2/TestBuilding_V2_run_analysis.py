from TestBuilding_V2_model import build_model
import openseespy.opensees as ops
import numpy as np


def run_analysis():
    print('\n--- Starting Static Analysis ---')
    try:
        ops.system('BandGeneral')
        ops.numberer('RCM')
        ops.constraints('Plain')
        ops.integrator('LoadControl', 1.0 / 15)
        ops.algorithm('Linear')
        ops.analysis('Static')
        ops.analyze(15)
        print('Static analysis completed successfully.')
    except Exception as e:
        print(f'Error in static analysis: {e}')

    print('\n--- Starting Modal Analysis ---')
    try:
        ops.setTime(0.0)
        ops.remove('loadPattern', 1)

        num_modes = 10
        eigen_values = ops.eigen(num_modes)
        print('Modal Periods (s):')
        for i, val in enumerate(eigen_values):
            if val > 1e-6:
                freq = np.sqrt(val) / (2 * np.pi)
                period = 1.0 / freq
                print(f'  - Mode {i+1}: {period:.4f} s')
        print('Modal analysis completed successfully.')
    except Exception as e:
        print(f'Error in modal analysis: {e}')


if __name__ == '__main__':
    build_model()
    print('Model built successfully.')
    run_analysis()