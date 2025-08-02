# 🎛️ Control de Visualización

## Configuración de Visualización

### Estructura de Configuración
```python
'visualization': {
    'enabled': False,           # Control maestro on/off
    'static_deformed': False,   # Deformada estática
    'modal_shapes': False,      # Formas modales  
    'max_modes': 6,            # Máximo número de modos a visualizar
    'deform_scale': 100,       # Factor de escala visual
    'export_format': 'html',   # Formato de exportación
    'show_nodes': True,        # Mostrar nodos
    'line_width': 2            # Grosor de líneas
}
```

## Parámetros de Visualización

### Parámetros Básicos

| Parámetro | Tipo | Descripción | Valores |
|-----------|------|-------------|---------|
| `enabled` | bool | Control maestro de visualización | `True/False` |
| `static_deformed` | bool | Generar deformada estática | `True/False` |
| `modal_shapes` | bool | Generar formas modales | `True/False` |
| `max_modes` | int | Número máximo de modos a visualizar | `1-20` |

### Parámetros de Estilo

| Parámetro | Tipo | Descripción | Valores |
|-----------|------|-------------|---------|
| `deform_scale` | float | Factor de escala de deformación | `1-1000` |
| `export_format` | str | Formato de archivo de salida | `'html', 'png'` |
| `show_nodes` | bool | Mostrar nodos en la visualización | `True/False` |
| `line_width` | float | Grosor de líneas estructurales | `0.5-5.0` |

### Parámetros de Color

| Parámetro | Tipo | Descripción | Valores |
|-----------|------|-------------|---------|
| `beam_color` | str | Color de vigas | `'blue', '#0000FF'` |
| `column_color` | str | Color de columnas | `'red', '#FF0000'` |
| `background_color` | str | Color de fondo | `'white', '#FFFFFF'` |

## Casos de Uso Específicos

### 1. Análisis de Producción (Sin Visualización)
```python
viz_config = {
    'enabled': False
}
# Resultado: Solo datos numéricos, máxima velocidad
```

### 2. Verificación Rápida (Solo Deformada)
```python
viz_config = {
    'enabled': True,
    'static_deformed': True,
    'modal_shapes': False,
    'deform_scale': 50
}
# Resultado: 1 archivo HTML con deformada estática
```

### 3. Análisis Modal Completo
```python
viz_config = {
    'enabled': True,
    'static_deformed': False,
    'modal_shapes': True,
    'max_modes': 10,
    'deform_scale': 100
}
# Resultado: 10 archivos HTML con formas modales
```

### 4. Presentación Ejecutiva
```python
viz_config = {
    'enabled': True,
    'static_deformed': True,
    'modal_shapes': True,
    'max_modes': 6,
    'deform_scale': 200,
    'show_nodes': True,
    'line_width': 3,
    'beam_color': 'blue',
    'column_color': 'red'
}
# Resultado: Visualizaciones completas y estilizadas
```

### 5. Análisis de Investigación
```python
viz_config = {
    'enabled': True,
    'static_deformed': True,
    'modal_shapes': True,
    'max_modes': 15,
    'deform_scale': 150,
    'export_format': 'html',
    'background_color': 'white'
}
# Resultado: Visualizaciones detalladas para análisis
```

## Archivos de Salida

### Nomenclatura de Archivos
```
results/
├── modelo_results.json                    # Resultados numéricos
├── modelo_static_deformed.html           # Deformada estática
├── modelo_mode_1_T0.2500s.html          # Modo 1 con período
├── modelo_mode_2_T0.1800s.html          # Modo 2 con período
└── modelo_mode_N_T0.XXXXs.html          # Modo N con período
```

### Estructura de Archivos HTML
- **Interactividad**: Zoom, rotación, pan
- **Información**: Tooltips con datos del nodo/elemento
- **Escalado**: Automático y manual
- **Exportación**: PNG desde el navegador

## Optimización de Performance

### Para Estudios Grandes (1000+ modelos)
```python
# Configuración optimizada para velocidad
viz_config = {
    'enabled': False  # Sin visualización
}
# Tiempo estimado: 50-70% más rápido
```

### Para Verificación Intermedia (100-500 modelos)
```python
# Configuración balanceada
viz_config = {
    'enabled': True,
    'static_deformed': True,
    'modal_shapes': False  # Solo deformadas estáticas
}
# Tiempo estimado: 20-30% más lento que sin visualización
```

### Para Estudios Detallados (10-50 modelos)
```python
# Configuración completa
viz_config = {
    'enabled': True,
    'static_deformed': True,
    'modal_shapes': True,
    'max_modes': 12
}
# Tiempo estimado: 2-3x más lento, pero información completa
```

## Configuración Dinámica

### Configuración Basada en Parámetros del Modelo
```python
def get_dynamic_viz_config(L_B_ratio, B, nx, ny):
    """Configuración de visualización basada en complejidad del modelo"""
    
    # Calcular complejidad del modelo
    complexity = nx * ny * L_B_ratio
    
    if complexity < 20:  # Modelos simples
        return {
            'enabled': True,
            'static_deformed': True,
            'modal_shapes': True,
            'max_modes': 8
        }
    elif complexity < 50:  # Modelos medianos
        return {
            'enabled': True,
            'static_deformed': True,
            'modal_shapes': False
        }
    else:  # Modelos complejos
        return {
            'enabled': False
        }
```

### Configuración Basada en Propósito
```python
def get_purpose_viz_config(purpose):
    """Configuración basada en el propósito del análisis"""
    
    configs = {
        'production': {'enabled': False},
        'verification': {
            'enabled': True,
            'static_deformed': True,
            'modal_shapes': False
        },
        'research': {
            'enabled': True,
            'static_deformed': True,
            'modal_shapes': True,
            'max_modes': 12
        },
        'presentation': {
            'enabled': True,
            'static_deformed': True,
            'modal_shapes': True,
            'max_modes': 6,
            'deform_scale': 200,
            'line_width': 3
        }
    }
    
    return configs.get(purpose, {'enabled': False})
```

## Solución de Problemas

### Visualización no se Genera
1. **Verificar que enabled = True**
2. **Confirmar que el análisis fue exitoso**
3. **Revisar permisos de escritura en directorio results**
4. **Verificar instalación de opstool**

### Archivos HTML Vacíos o Corruptos
1. **Verificar versión de opstool**: `pip install --upgrade opstool`
2. **Revisar logs de error en el análisis**
3. **Confirmar que el modelo tiene elementos válidos**

### Performance Lenta con Visualización
1. **Reducir max_modes**: De 12 a 6 o menos
2. **Deshabilitar modal_shapes** para estudios grandes
3. **Usar deform_scale más bajo**: Menos cálculos de renderizado

### Archivos HTML Muy Grandes
1. **Reducir deform_scale**: Menos detalle visual
2. **Usar show_nodes = False**: Menos elementos a renderizar
3. **Considerar export_format = 'png'** para archivos estáticos más pequeños
