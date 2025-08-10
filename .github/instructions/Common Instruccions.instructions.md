---
applyTo: '**'
---
We are working with in a dev python environment, our library is called opsparametric so when you make imports from this library, use the following format:

```python
from opsparametric import ModelBuilder
from opsparametric import PythonExporter
from opsparametric import Domain
```
Do not make imports like this:

```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from model_builder import ModelBuilder
from python_exporter import PythonExporter
from domain import Domain
```
When you are writing code, please ensure that you use the correct import paths as shown above. This will help maintain consistency across our codebase and ensure that all modules are correctly referenced.

When you want to try new tests make sure to use test folder, the same goes for examples, use the examples folder.