# Propuesta de Estructura Mejorada

## 1. Separar Factory de Domain Objects

### ModelBuilder (Factory) - Lo que tienes ahora está bien
```python
class ModelBuilder:
    """Factory para crear modelos - mantiene lógica de construcción"""
    
    def create_model(self, params) -> StructuralModel:
        # Orquesta la creación usando domain objects
        geometry = GeometryBuilder.create(params)
        sections = SectionBuilder.create(params)
        loads = LoadBuilder.create(geometry, params)
        analysis_config = AnalysisConfigBuilder.create(params)
        
        return StructuralModel(geometry, sections, loads, analysis_config)
```

### Domain Objects (Nuevos)
```python
@dataclass
class StructuralModel:
    """Representa un modelo estructural completo"""
    geometry: Geometry
    sections: Sections
    loads: Loads
    analysis_config: AnalysisConfig
    name: str
    
    def to_dict(self) -> Dict:
        """Serializa a diccionario para JSON"""
        
    def save(self, filepath: str):
        """Guarda el modelo en archivo"""

@dataclass 
class Geometry:
    """Representa la geometría del modelo"""
    nodes: Dict[int, Node]
    elements: Dict[int, Element]
    L: float
    B: float
    nx: int
    ny: int
    
    def get_boundary_nodes(self) -> List[Node]:
        """Obtiene nodos del contorno"""
        
    def get_floor_nodes(self, floor: int) -> List[Node]:
        """Obtiene nodos de un piso específico"""

class Node:
    def __init__(self, tag: int, coords: List[float], floor: int):
        self.tag = tag
        self.coords = coords
        self.floor = floor
        self.grid_pos = None
```

## 2. Builders Especializados (Single Responsibility)

```python
class GeometryBuilder:
    """Construye la geometría del modelo"""
    
    @staticmethod
    def create(L_B_ratio: float, B: float, nx: int, ny: int, 
               num_floors: int, floor_height: float) -> Geometry:
        nodes = GeometryBuilder._create_nodes(...)
        elements = GeometryBuilder._create_elements(...)
        return Geometry(nodes, elements, L, B, nx, ny)
    
    @staticmethod
    def _create_nodes(...) -> Dict[int, Node]:
        """Lógica específica de creación de nodos"""
        
    @staticmethod
    def _create_elements(...) -> Dict[int, Element]:
        """Lógica específica de creación de elementos"""

class SectionBuilder:
    """Construye las secciones del modelo"""
    
    @staticmethod
    def create(fixed_params: Dict) -> Sections:
        # Lógica específica de secciones

class LoadBuilder:
    """Construye las cargas del modelo"""
    
    @staticmethod
    def create(geometry: Geometry, load_params: Dict) -> Loads:
        # Lógica específica de cargas
```

## 3. Analysis Configuration como First-Class Object

```python
@dataclass
class AnalysisConfig:
    """Configuración de análisis como objeto de primera clase"""
    enabled_analyses: List[str]
    static_config: Optional[StaticConfig]
    modal_config: Optional[ModalConfig]
    dynamic_config: Optional[DynamicConfig]
    visualization_config: VisualizationConfig
    
    def get_solver_config(self, analysis_type: str) -> Dict:
        """Obtiene configuración del solver para un tipo de análisis"""
        
    def is_enabled(self, analysis_type: str) -> bool:
        """Verifica si un análisis está habilitado"""

@dataclass
class StaticConfig:
    system: str = 'BandGeneral'
    numberer: str = 'RCM'
    constraints: str = 'Plain'
    integrator: str = 'LoadControl'
    algorithm: str = 'Linear'
    analysis: str = 'Static'
    steps: int = 10
```

## 4. ModelBuilder Refactorizado

```python
class ModelBuilder:
    """
    Factory mejorado - orquesta la creación usando builders especializados
    """
    
    def __init__(self, output_dir: str = "models"):
        self.output_dir = output_dir
        self.fixed_params = {...}  # Mantiene parámetros fijos
        
    def create_model(self, L_B_ratio: float, B: float, nx: int, ny: int,
                    enabled_analyses: List[str] = None,
                    analysis_params: Dict = None) -> StructuralModel:
        """
        Crea un modelo usando builders especializados
        """
        # Calcular dimensiones
        L, B = self.calculate_dimensions(L_B_ratio, B)
        
        # Crear componentes usando builders especializados
        geometry = GeometryBuilder.create(
            L_B_ratio, B, nx, ny, 
            self.fixed_params['num_floors'],
            self.fixed_params['floor_height']
        )
        
        sections = SectionBuilder.create(self.fixed_params)
        
        loads = LoadBuilder.create(geometry, {'distributed_load': 1.0})
        
        analysis_config = AnalysisConfigBuilder.create(
            enabled_analyses or ['static', 'modal'],
            analysis_params or {}
        )
        
        # Crear y guardar modelo
        model_name = self.generate_model_name(L_B_ratio, B, nx, ny)
        model = StructuralModel(
            geometry=geometry,
            sections=sections, 
            loads=loads,
            analysis_config=analysis_config,
            name=model_name
        )
        
        # Guardar en archivo
        model_file = os.path.join(self.output_dir, f"{model_name}.json")
        model.save(model_file)
        
        return model
```

## Ventajas de Esta Estructura

### 1. **Single Responsibility Principle**
- Cada builder tiene una sola responsabilidad
- Cada domain object representa un concepto del dominio

### 2. **Mejor Testabilidad**
- Puedes testear cada builder independientemente
- Los domain objects son fáciles de mockear

### 3. **Reutilización**
- Los builders pueden reutilizarse en diferentes contextos
- Los domain objects pueden extenderse fácilmente

### 4. **Mantenibilidad**
- Cambios en geometría solo afectan GeometryBuilder
- Cambios en análisis solo afectan AnalysisConfigBuilder

### 5. **Expresividad**
- El código es más legible y autodocumentado
- Las relaciones entre objetos son más claras

## Migración Gradual

Puedes implementar esto gradualmente:

1. **Paso 1**: Crear los domain objects (StructuralModel, Geometry, etc.)
2. **Paso 2**: Crear builders especializados
3. **Paso 3**: Refactorizar ModelBuilder para usar los nuevos builders
4. **Paso 4**: Actualizar tests y documentación

Esta estructura mantiene todos los beneficios de tu diseño actual pero mejora la organización y mantenibilidad del código.
