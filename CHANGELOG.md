# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere al [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Preparación para release inicial en PyPI
- Configuración de GitHub Actions para CI/CD
- Documentación completa del proyecto

## [1.0.0] - 2025-08-02

### Added
- Sistema completo de análisis paramétrico para OpenSees
- Arquitectura modular refactorizada
- Soporte para análisis estático, modal y dinámico
- Control granular de visualización con opstool
- Suite completa de tests
- Documentación detallada en carpeta `docs/`
- Ejemplos prácticos en carpeta `examples/`
- Jupyter notebooks para casos de uso
- Exportación automática de scripts Python
- Generación de reportes automáticos

### Features
- **ModelBuilder**: Constructor unificado de modelos
- **AnalysisEngine**: Motor de análisis refactorizado  
- **ParametricRunner**: Orquestador de estudios paramétricos
- **PythonExporter**: Exportador de scripts Python standalone
- **ReportGenerator**: Generador de reportes automáticos
- **Visualization Helper**: Control granular de visualizaciones

### Technical Details
- Geometría: Estructuras rectangulares con relación L/B variable
- Elementos: Columnas 40x40 cm, vigas 25x40 cm, losa 10 cm
- Pisos: 2 pisos de 3 m cada uno
- Materiales: Hormigón armado con propiedades configurables
- Análisis: Estático (cargas gravitatorias), modal y dinámico

### Dependencies
- openseespy >= 3.4.0
- opstool >= 0.0.1  
- numpy >= 1.21.0
- pandas >= 1.3.0
- matplotlib >= 3.5.0
- plotly >= 5.0.0
- jupyter >= 1.0.0
- ipywidgets >= 7.6.0
- tqdm >= 4.62.0
