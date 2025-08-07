import openseespy.opensees as ops
import numpy as np

def build_model():
    # Limpiar modelo anterior
    ops.wipe()
    ops.model('basic', '-ndm', 3, '-ndf', 6)

    # Parámetros del modelo
    L, B = 12.0, 9.0  # Dimensiones
    nx, ny = 3, 2  # Ejes
    E = 2173706.5119284154  # Módulo de elasticidad
    nu = 0.2  # Coeficiente de Poisson
    G = E / (2 * (1 + nu))  # Módulo de corte
    thickness = 0.15  # Espesor de losa
    rho = 2500  # Densidad

    # Crear nodos
    ops.node(1, 0.0, 0.0, 0.0)
    ops.node(2, 4.0, 0.0, 0.0)
    ops.node(3, 8.0, 0.0, 0.0)
    ops.node(4, 12.0, 0.0, 0.0)
    ops.node(5, 0.0, 4.5, 0.0)
    ops.node(6, 4.0, 4.5, 0.0)
    ops.node(7, 8.0, 4.5, 0.0)
    ops.node(8, 12.0, 4.5, 0.0)
    ops.node(9, 0.0, 9.0, 0.0)
    ops.node(10, 4.0, 9.0, 0.0)
    ops.node(11, 8.0, 9.0, 0.0)
    ops.node(12, 12.0, 9.0, 0.0)
    ops.node(13, 0.0, 0.0, 3.5)
    ops.node(14, 4.0, 0.0, 3.5)
    ops.node(15, 8.0, 0.0, 3.5)
    ops.node(16, 12.0, 0.0, 3.5)
    ops.node(17, 0.0, 4.5, 3.5)
    ops.node(18, 4.0, 4.5, 3.5)
    ops.node(19, 8.0, 4.5, 3.5)
    ops.node(20, 12.0, 4.5, 3.5)
    ops.node(21, 0.0, 9.0, 3.5)
    ops.node(22, 4.0, 9.0, 3.5)
    ops.node(23, 8.0, 9.0, 3.5)
    ops.node(24, 12.0, 9.0, 3.5)
    ops.node(25, 0.0, 0.0, 7.0)
    ops.node(26, 4.0, 0.0, 7.0)
    ops.node(27, 8.0, 0.0, 7.0)
    ops.node(28, 12.0, 0.0, 7.0)
    ops.node(29, 0.0, 4.5, 7.0)
    ops.node(30, 4.0, 4.5, 7.0)
    ops.node(31, 8.0, 4.5, 7.0)
    ops.node(32, 12.0, 4.5, 7.0)
    ops.node(33, 0.0, 9.0, 7.0)
    ops.node(34, 4.0, 9.0, 7.0)
    ops.node(35, 8.0, 9.0, 7.0)
    ops.node(36, 12.0, 9.0, 7.0)
    ops.node(37, 0.0, 0.0, 10.5)
    ops.node(38, 4.0, 0.0, 10.5)
    ops.node(39, 8.0, 0.0, 10.5)
    ops.node(40, 12.0, 0.0, 10.5)
    ops.node(41, 0.0, 4.5, 10.5)
    ops.node(42, 4.0, 4.5, 10.5)
    ops.node(43, 8.0, 4.5, 10.5)
    ops.node(44, 12.0, 4.5, 10.5)
    ops.node(45, 0.0, 9.0, 10.5)
    ops.node(46, 4.0, 9.0, 10.5)
    ops.node(47, 8.0, 9.0, 10.5)
    ops.node(48, 12.0, 9.0, 10.5)

    # Crear materiales y secciones basadas en el modelo
    # Transformaciones geométricas
    ops.geomTransf('Linear', 4, 0, 1, 0)
    ops.geomTransf('Linear', 5, 0, 0, 1)

    # Secciones basadas en el modelo
    ops.section('ElasticMembranePlateSection', 1, E, nu, 0.1, rho)
    # Sección 2 - column
    w_2, h_2 = 0.4, 0.4
    A_2 = w_2 * h_2
    Iz_2 = w_2 * h_2**3 / 12
    Iy_2 = h_2 * w_2**3 / 12
    # Constante torsional (aproximación rectangular)
    a_2, b_2 = max(w_2, h_2), min(w_2, h_2)
    J_2 = a_2 * b_2**3 * (1/3 - 0.21 * (b_2/a_2) * (1 - (b_2**4)/(12*a_2**4)))
    ops.section('Elastic', 2, E, A_2, Iz_2, Iy_2, G, J_2)

    # Sección 3 - beam
    w_3, h_3 = 0.25, 0.4
    A_3 = w_3 * h_3
    Iz_3 = w_3 * h_3**3 / 12
    Iy_3 = h_3 * w_3**3 / 12
    # Constante torsional (aproximación rectangular)
    a_3, b_3 = max(w_3, h_3), min(w_3, h_3)
    J_3 = a_3 * b_3**3 * (1/3 - 0.21 * (b_3/a_3) * (1 - (b_3**4)/(12*a_3**4)))
    ops.section('Elastic', 3, E, A_3, Iz_3, Iy_3, G, J_3)


    # Crear elementos
    ops.element('ShellMITC4', 1, *[13, 14, 18, 17], 1)
    ops.element('ShellMITC4', 2, *[14, 15, 19, 18], 1)
    ops.element('ShellMITC4', 3, *[15, 16, 20, 19], 1)
    ops.element('ShellMITC4', 4, *[17, 18, 22, 21], 1)
    ops.element('ShellMITC4', 5, *[18, 19, 23, 22], 1)
    ops.element('ShellMITC4', 6, *[19, 20, 24, 23], 1)
    ops.element('ShellMITC4', 7, *[25, 26, 30, 29], 1)
    ops.element('ShellMITC4', 8, *[26, 27, 31, 30], 1)
    ops.element('ShellMITC4', 9, *[27, 28, 32, 31], 1)
    ops.element('ShellMITC4', 10, *[29, 30, 34, 33], 1)
    ops.element('ShellMITC4', 11, *[30, 31, 35, 34], 1)
    ops.element('ShellMITC4', 12, *[31, 32, 36, 35], 1)
    ops.element('ShellMITC4', 13, *[37, 38, 42, 41], 1)
    ops.element('ShellMITC4', 14, *[38, 39, 43, 42], 1)
    ops.element('ShellMITC4', 15, *[39, 40, 44, 43], 1)
    ops.element('ShellMITC4', 16, *[41, 42, 46, 45], 1)
    ops.element('ShellMITC4', 17, *[42, 43, 47, 46], 1)
    ops.element('ShellMITC4', 18, *[43, 44, 48, 47], 1)
    # Error: No se encontró transf_tag para sección 2 en elemento 19
    # ops.element('elasticBeamColumn', 19, *[1, 13], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 20
    # ops.element('elasticBeamColumn', 20, *[13, 25], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 21
    # ops.element('elasticBeamColumn', 21, *[25, 37], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 22
    # ops.element('elasticBeamColumn', 22, *[2, 14], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 23
    # ops.element('elasticBeamColumn', 23, *[14, 26], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 24
    # ops.element('elasticBeamColumn', 24, *[26, 38], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 25
    # ops.element('elasticBeamColumn', 25, *[3, 15], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 26
    # ops.element('elasticBeamColumn', 26, *[15, 27], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 27
    # ops.element('elasticBeamColumn', 27, *[27, 39], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 28
    # ops.element('elasticBeamColumn', 28, *[4, 16], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 29
    # ops.element('elasticBeamColumn', 29, *[16, 28], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 30
    # ops.element('elasticBeamColumn', 30, *[28, 40], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 31
    # ops.element('elasticBeamColumn', 31, *[5, 17], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 32
    # ops.element('elasticBeamColumn', 32, *[17, 29], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 33
    # ops.element('elasticBeamColumn', 33, *[29, 41], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 34
    # ops.element('elasticBeamColumn', 34, *[6, 18], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 35
    # ops.element('elasticBeamColumn', 35, *[18, 30], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 36
    # ops.element('elasticBeamColumn', 36, *[30, 42], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 37
    # ops.element('elasticBeamColumn', 37, *[7, 19], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 38
    # ops.element('elasticBeamColumn', 38, *[19, 31], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 39
    # ops.element('elasticBeamColumn', 39, *[31, 43], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 40
    # ops.element('elasticBeamColumn', 40, *[8, 20], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 41
    # ops.element('elasticBeamColumn', 41, *[20, 32], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 42
    # ops.element('elasticBeamColumn', 42, *[32, 44], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 43
    # ops.element('elasticBeamColumn', 43, *[9, 21], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 44
    # ops.element('elasticBeamColumn', 44, *[21, 33], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 45
    # ops.element('elasticBeamColumn', 45, *[33, 45], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 46
    # ops.element('elasticBeamColumn', 46, *[10, 22], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 47
    # ops.element('elasticBeamColumn', 47, *[22, 34], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 48
    # ops.element('elasticBeamColumn', 48, *[34, 46], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 49
    # ops.element('elasticBeamColumn', 49, *[11, 23], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 50
    # ops.element('elasticBeamColumn', 50, *[23, 35], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 51
    # ops.element('elasticBeamColumn', 51, *[35, 47], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 52
    # ops.element('elasticBeamColumn', 52, *[12, 24], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 53
    # ops.element('elasticBeamColumn', 53, *[24, 36], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 2 en elemento 54
    # ops.element('elasticBeamColumn', 54, *[36, 48], 2, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 55
    # ops.element('elasticBeamColumn', 55, *[13, 14], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 56
    # ops.element('elasticBeamColumn', 56, *[14, 15], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 57
    # ops.element('elasticBeamColumn', 57, *[15, 16], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 58
    # ops.element('elasticBeamColumn', 58, *[17, 18], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 59
    # ops.element('elasticBeamColumn', 59, *[18, 19], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 60
    # ops.element('elasticBeamColumn', 60, *[19, 20], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 61
    # ops.element('elasticBeamColumn', 61, *[21, 22], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 62
    # ops.element('elasticBeamColumn', 62, *[22, 23], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 63
    # ops.element('elasticBeamColumn', 63, *[23, 24], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 64
    # ops.element('elasticBeamColumn', 64, *[13, 17], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 65
    # ops.element('elasticBeamColumn', 65, *[14, 18], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 66
    # ops.element('elasticBeamColumn', 66, *[15, 19], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 67
    # ops.element('elasticBeamColumn', 67, *[16, 20], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 68
    # ops.element('elasticBeamColumn', 68, *[17, 21], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 69
    # ops.element('elasticBeamColumn', 69, *[18, 22], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 70
    # ops.element('elasticBeamColumn', 70, *[19, 23], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 71
    # ops.element('elasticBeamColumn', 71, *[20, 24], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 72
    # ops.element('elasticBeamColumn', 72, *[25, 26], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 73
    # ops.element('elasticBeamColumn', 73, *[26, 27], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 74
    # ops.element('elasticBeamColumn', 74, *[27, 28], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 75
    # ops.element('elasticBeamColumn', 75, *[29, 30], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 76
    # ops.element('elasticBeamColumn', 76, *[30, 31], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 77
    # ops.element('elasticBeamColumn', 77, *[31, 32], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 78
    # ops.element('elasticBeamColumn', 78, *[33, 34], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 79
    # ops.element('elasticBeamColumn', 79, *[34, 35], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 80
    # ops.element('elasticBeamColumn', 80, *[35, 36], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 81
    # ops.element('elasticBeamColumn', 81, *[25, 29], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 82
    # ops.element('elasticBeamColumn', 82, *[26, 30], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 83
    # ops.element('elasticBeamColumn', 83, *[27, 31], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 84
    # ops.element('elasticBeamColumn', 84, *[28, 32], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 85
    # ops.element('elasticBeamColumn', 85, *[29, 33], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 86
    # ops.element('elasticBeamColumn', 86, *[30, 34], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 87
    # ops.element('elasticBeamColumn', 87, *[31, 35], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 88
    # ops.element('elasticBeamColumn', 88, *[32, 36], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 89
    # ops.element('elasticBeamColumn', 89, *[37, 38], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 90
    # ops.element('elasticBeamColumn', 90, *[38, 39], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 91
    # ops.element('elasticBeamColumn', 91, *[39, 40], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 92
    # ops.element('elasticBeamColumn', 92, *[41, 42], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 93
    # ops.element('elasticBeamColumn', 93, *[42, 43], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 94
    # ops.element('elasticBeamColumn', 94, *[43, 44], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 95
    # ops.element('elasticBeamColumn', 95, *[45, 46], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 96
    # ops.element('elasticBeamColumn', 96, *[46, 47], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 97
    # ops.element('elasticBeamColumn', 97, *[47, 48], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 98
    # ops.element('elasticBeamColumn', 98, *[37, 41], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 99
    # ops.element('elasticBeamColumn', 99, *[38, 42], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 100
    # ops.element('elasticBeamColumn', 100, *[39, 43], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 101
    # ops.element('elasticBeamColumn', 101, *[40, 44], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 102
    # ops.element('elasticBeamColumn', 102, *[41, 45], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 103
    # ops.element('elasticBeamColumn', 103, *[42, 46], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 104
    # ops.element('elasticBeamColumn', 104, *[43, 47], 3, TRANSF_TAG_MISSING)
    # Error: No se encontró transf_tag para sección 3 en elemento 105
    # ops.element('elasticBeamColumn', 105, *[44, 48], 3, TRANSF_TAG_MISSING)

    # Aplicar restricciones en la base
    ops.fix(1, 1, 1, 1, 1, 1, 1)
    ops.fix(2, 1, 1, 1, 1, 1, 1)
    ops.fix(3, 1, 1, 1, 1, 1, 1)
    ops.fix(4, 1, 1, 1, 1, 1, 1)
    ops.fix(5, 1, 1, 1, 1, 1, 1)
    ops.fix(6, 1, 1, 1, 1, 1, 1)
    ops.fix(7, 1, 1, 1, 1, 1, 1)
    ops.fix(8, 1, 1, 1, 1, 1, 1)
    ops.fix(9, 1, 1, 1, 1, 1, 1)
    ops.fix(10, 1, 1, 1, 1, 1, 1)
    ops.fix(11, 1, 1, 1, 1, 1, 1)
    ops.fix(12, 1, 1, 1, 1, 1, 1)
    # Aplicar cargas
    ops.timeSeries('Linear', 1)
    ops.pattern('Plain', 1, 1)
    ops.load(37, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0)
    ops.load(38, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0)
    ops.load(39, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0)
    ops.load(40, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0)
    ops.load(41, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0)
    ops.load(42, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0)
    ops.load(43, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0)
    ops.load(44, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0)
    ops.load(45, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0)
    ops.load(46, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0)
    ops.load(47, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0)
    ops.load(48, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0)

if __name__ == '__main__':
    build_model()
    print('Modelo construido y listo para ser importado.')