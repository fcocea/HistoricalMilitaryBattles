<h2 align="center"> Batallas militares históricas</h3>
<p align="center">
Condiciones y resultados de más de 600 batallas libradas entre 1600 y 1973 d.C.
</p>

### Descripción
Este proyecto tiene como objetivo analizar las condiciones y resultados de más de 600 batallas libradas entre 1600 y 1973 d.C. Mediante el uso de técnicas de visualización de datos, se busca identificar patrones y tendencias en la historia de las guerras.

### Requerimientos
- [Python ^3.10](https://www.python.org/downloads/) 
- [Poetry](https://python-poetry.org/docs/#installation) (Opcional)

### Instalación
1. Clonar el repositorio
```bash
git clone https://github.com/fcocea/HistoricalMilitaryBattles
```
---

2. Instalar las dependencias (Poetry)
```bash
cd HistoricalMilitaryBattles
poetry install
```
3. Lanzar el dashboard (Poetry)
```bash
poetry run python3 app.py
```

---

De ser necesario, también es posible crear un entorno virtual de Python y lanzar el dashboard de la siguiente manera:

1. Crear un entorno virtual (Opcional)
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instalar las dependencias
```bash
cd HistoricalMilitaryBattles
pip install -r requirements.txt
```
3. Lanzar el dashboard
```bash
python3 app.py
```
---
4. El dashboard estará disponible en la dirección [http:// localhost:8050](http://localhost:8050)

En caso de un error en el lanzamiento, establece la siguiente variable de entorno:
```bash
export REACT_VERSION=18.2.0
```
y vuelve a lanzar el dashboard.


#### Créditos
Proyecto realizado por:
- Oscar Castillo
- Francisco Cea
- Luis Valenzuela