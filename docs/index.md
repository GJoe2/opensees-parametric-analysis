# 📚 Índice de Documentación

## Documentación Organizada del Sistema OpenSees

Esta carpeta contiene la documentación detallada del Sistema de Análisis Paramétrico OpenSees, organizada por temas específicos para facilitar la consulta y el mantenimiento.

## 📋 Estructura de la Documentación

| Archivo | Descripción | Audiencia |
|---------|-------------|-----------|
| [**architecture.md**](architecture.md) | Arquitectura del sistema, componentes y diseño | Desarrolladores, Arquitectos |
| [**installation.md**](installation.md) | Instalación, configuración y dependencias | Usuarios nuevos, Administradores |
| [**usage.md**](usage.md) | Guía de uso, ejemplos y API | Usuarios finales, Investigadores |
| [**visualization.md**](visualization.md) | Control de visualización y configuración | Usuarios avanzados |
| [**model-parameters.md**](model-parameters.md) | Parámetros del modelo y nomenclatura | Ingenieros, Investigadores |
| [**testing.md**](testing.md) | Suite de tests y validación | Desarrolladores, QA |
| [**troubleshooting.md**](troubleshooting.md) | Solución de problemas comunes | Todos los usuarios |

## 🚀 Guías de Inicio Rápido

### Para Usuarios Nuevos
1. [**Instalación**](installation.md) - Configurar el entorno
2. [**Uso Básico**](usage.md#análisis-individual-rápido) - Primer análisis
3. [**Parámetros**](model-parameters.md) - Entender el modelo

### Para Desarrolladores
1. [**Arquitectura**](architecture.md) - Entender el diseño
2. [**Testing**](testing.md) - Ejecutar y crear tests
3. [**Troubleshooting**](troubleshooting.md) - Debugging avanzado

### Para Investigadores
1. [**Parámetros**](model-parameters.md) - Configurar estudios
2. [**Uso Avanzado**](usage.md#estudios-paramétricos) - Estudios paramétricos
3. [**Visualización**](visualization.md) - Control de salidas

## 🎯 Casos de Uso Específicos

### Análisis Individual
- [Análisis sin visualización](usage.md#análisis-básico-sin-visualización) - Máxima velocidad
- [Análisis con visualización](usage.md#análisis-con-visualización-completa) - Verificación visual
- [Configuración personalizada](usage.md#configuración-avanzada) - Control total

### Estudios Paramétricos
- [Estudio básico](usage.md#estudio-paramétrico-básico) - Pocas variables
- [Estudio completo](usage.md#estudio-paramétrico-avanzado) - Todas las combinaciones
- [Optimización de performance](visualization.md#optimización-de-performance) - Estudios grandes

### Visualización
- [Configuración por casos](visualization.md#casos-de-uso-específicos) - Según necesidad
- [Configuración dinámica](visualization.md#configuración-dinámica) - Automática
- [Solución de problemas](visualization.md#solución-de-problemas) - Debugging

## 🔧 Referencias Técnicas

### API del Sistema
- [ModelBuilder API](usage.md#api-unificada-de-modelbuilder) - Constructor de modelos
- [AnalysisEngine](architecture.md#⚙️-analysisengine-motor-de-análisis-refactorizado) - Motor de análisis
- [ParametricRunner](usage.md#estudios-paramétricos) - Orquestador

### Configuración Avanzada
- [Parámetros de análisis](model-parameters.md#configuración-de-análisis) - Estático, modal, dinámico
- [Parámetros de visualización](visualization.md#parámetros-de-visualización) - Control granular
- [Validación de parámetros](model-parameters.md#validación-de-parámetros) - Rangos válidos

### Extensibilidad
- [Agregar análisis](architecture.md#agregar-nuevo-tipo-de-análisis) - Nuevos tipos
- [Agregar visualización](architecture.md#agregar-nueva-visualización) - Nuevas vistas
- [Modificar parámetros](architecture.md#modificar-parámetros-del-modelo) - Personalización

## 🧪 Testing y Validación

### Ejecutar Tests
- [Runner interactivo](testing.md#opción-1-runner-interactivo) - Menú de tests
- [Pytest](testing.md#opción-2-pytest-recomendado) - Herramienta profesional
- [Tests específicos](testing.md#opción-3-tests-específicos-con-runner) - Por componente

### Tipos de Tests
- [Tests unitarios](testing.md#test-modelbuilder) - Funciones individuales
- [Tests de integración](testing.md#integración-✅) - Flujos completos
- [Tests de performance](testing.md#tests-de-performance) - Velocidad y memoria

## 🐛 Solución de Problemas

### Por Categoría
- [Instalación](troubleshooting.md#1-problemas-de-instalación) - Dependencias y setup
- [Análisis](troubleshooting.md#2-problemas-de-análisis) - Convergencia y cálculo
- [Visualización](troubleshooting.md#3-problemas-de-visualización) - Archivos HTML
- [Performance](troubleshooting.md#4-problemas-de-performance) - Velocidad y memoria
- [Archivos](troubleshooting.md#5-problemas-de-archivos) - JSON y paths

### Herramientas de Diagnóstico
- [Logging detallado](troubleshooting.md#habilitar-logging-detallado) - Debug avanzado
- [Diagnóstico del sistema](troubleshooting.md#verificar-estado-del-sistema) - Verificación completa

## 📊 Mejores Prácticas

### Desarrollo
- [Separación de responsabilidades](architecture.md#separación-de-responsabilidades) - Diseño modular
- [Tests independientes](testing.md#1-tests-independientes) - Calidad de código
- [Configuración dinámica](visualization.md#configuración-dinámica) - Flexibilidad

### Uso en Producción
- [Optimización de estudios](visualization.md#para-estudios-grandes-1000-modelos) - Performance
- [Validación de parámetros](model-parameters.md#validación-de-parámetros) - Robustez
- [Manejo de errores](troubleshooting.md) - Recuperación

### Investigación
- [Combinaciones recomendadas](model-parameters.md#combinaciones-recomendadas) - Estudios efectivos
- [Control de visualización](visualization.md#casos-de-uso-específicos) - Según propósito
- [Generación de reportes](usage.md#generación-de-reportes) - Documentación

## 🔄 Mantenimiento de la Documentación

### Actualización
Esta documentación se mantiene sincronizada con el código. Al agregar nuevas funcionalidades:

1. **Actualizar la documentación correspondiente**
2. **Agregar ejemplos de uso**
3. **Incluir casos de test**
4. **Actualizar troubleshooting si es necesario**

### Contribuciones
Para contribuir a la documentación:

1. **Seguir la estructura existente**
2. **Incluir ejemplos prácticos**
3. **Mantener consistencia en el formato**
4. **Validar los ejemplos de código**

---

**Última actualización**: Agosto 2025  
**Versión del sistema**: Post-refactorización con arquitectura modular
