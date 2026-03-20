# Metricas de calidad para modelos de clasificacion

Este documento explica que son las metricas de calidad en clasificacion y como aplicarlas al modelo de practica (Gradient Boosting con vinos).

## 1. Que son las metricas de calidad

Las metricas de calidad son medidas numericas para evaluar que tan bien clasifica un modelo.

No basta con usar solo `accuracy` porque puede ocultar errores importantes, sobre todo cuando hay clases desbalanceadas.

## 2. Conceptos base

En clasificacion binaria:

- Clase `0`: baja calidad
- Clase `1`: alta calidad

Resultados posibles:

- `TP` (True Positive): predijo 1 y era 1
- `TN` (True Negative): predijo 0 y era 0
- `FP` (False Positive): predijo 1 pero era 0
- `FN` (False Negative): predijo 0 pero era 1

## 3. Metricas principales

### 3.1 Accuracy (Exactitud)

Proporcion total de predicciones correctas.

Formula:

`(TP + TN) / (TP + TN + FP + FN)`

Uso: da una idea general, pero puede ser enganosa con desbalance.

### 3.2 Precision (Precision)

De todo lo que el modelo predijo como clase positiva (1), cuanto era realmente positivo.

Formula:

`TP / (TP + FP)`

Uso: importante cuando quieres evitar falsos positivos.

### 3.3 Recall (Sensibilidad)

De todos los positivos reales (1), cuantos detecto el modelo.

Formula:

`TP / (TP + FN)`

Uso: importante cuando quieres evitar perder casos positivos.

### 3.4 F1-Score

Media armonica entre precision y recall.

Formula:

`2 * (Precision * Recall) / (Precision + Recall)`

Uso: recomendada cuando hay desbalance porque combina ambos criterios.

### 3.5 ROC-AUC

Mide la capacidad del modelo para separar clases usando probabilidades.

Rango:

- `0.5`: similar a azar
- `1.0`: separacion perfecta

Uso: comparacion robusta entre modelos binarios.

### 3.6 Matriz de confusion

Tabla con conteos de TP, TN, FP y FN. Permite ver claramente en que tipo de error falla el modelo.

## 4. Ejemplo practico (idea intuitiva)

Supongamos 100 vinos:

- 70 son clase 0 (baja calidad)
- 30 son clase 1 (alta calidad)

Si un modelo predice todo como clase 0:

- Accuracy = 70%
- Recall para clase 1 = 0%

Conclusión: parece bueno por accuracy, pero en realidad no detecta ningun vino de alta calidad.

## 5. Implementacion en este proyecto

En el notebook se agrego una celda con:

- `accuracy_score`
- `precision_score`
- `recall_score`
- `f1_score`
- `roc_auc_score`
- `confusion_matrix`
- `classification_report`
- grafica de matriz de confusion con `ConfusionMatrixDisplay`

Codigo de referencia:

```python
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay,
)
import matplotlib.pyplot as plt

y_pred = model.predict(x_test)
y_proba = model.predict_proba(x_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_proba)

print(f"Accuracy : {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall   : {recall:.3f}")
print(f"F1-Score : {f1:.3f}")
print(f"ROC-AUC  : {roc_auc:.3f}")

cm = confusion_matrix(y_test, y_pred)
print(cm)
print(classification_report(y_test, y_pred, target_names=["Baja calidad (0)", "Alta calidad (1)"]))

ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Baja", "Alta"]).plot(cmap="Blues")
plt.title("Matriz de confusion - Gradient Boosting")
plt.show()
```

## 6. Explicacion detallada linea por linea del codigo

En esta seccion se explica cada linea del bloque de metricas para entender exactamente que hace, que recibe y que devuelve.

### 6.1 Importacion de funciones

```python
from sklearn.metrics import (
        accuracy_score,
        precision_score,
        recall_score,
        f1_score,
        roc_auc_score,
        confusion_matrix,
        classification_report,
        ConfusionMatrixDisplay,
)
import matplotlib.pyplot as plt
```

- `from sklearn.metrics import (...)`:
    importa desde `scikit-learn` todas las funciones de evaluacion que usaras para clasificacion.
- `accuracy_score`:
    calcula el porcentaje de aciertos globales.
- `precision_score`:
    mide que tan confiables son las predicciones positivas (clase 1).
- `recall_score`:
    mide cuantas instancias positivas reales detecta el modelo.
- `f1_score`:
    combina precision y recall en un solo valor balanceado.
- `roc_auc_score`:
    mide capacidad de separacion entre clases usando probabilidades.
- `confusion_matrix`:
    construye la tabla de conteos TN, FP, FN, TP.
- `classification_report`:
    genera un resumen de precision/recall/f1/soporte por clase.
- `ConfusionMatrixDisplay`:
    herramienta para graficar la matriz de confusion.
- `import matplotlib.pyplot as plt`:
    importa la libreria de graficos para mostrar la matriz visualmente.

### 6.2 Generar predicciones y probabilidades

```python
y_pred = model.predict(x_test)
y_proba = model.predict_proba(x_test)[:, 1]
```

- `model.predict(x_test)`:
    devuelve una prediccion discreta por muestra (`0` o `1`).
    `y_pred` tiene el mismo largo que `y_test`.
- `model.predict_proba(x_test)`:
    devuelve probabilidades por clase en una matriz de 2 columnas: `[P(clase 0), P(clase 1)]`.
- `[:, 1]`:
    selecciona solo la columna de probabilidad de la clase positiva (`1`, alta calidad).
    este vector es necesario para ROC-AUC.

### 6.3 Calcular las metricas

```python
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_proba)
```

- `accuracy_score(y_test, y_pred)`:
    compara valor real vs predicho y calcula fraccion de aciertos.
    rango: `0` a `1`.
- `precision_score(y_test, y_pred)`:
    usa TP y FP para responder: "de lo que predije como 1, cuanto era realmente 1".
- `recall_score(y_test, y_pred)`:
    usa TP y FN para responder: "de todos los 1 reales, cuantos encontre".
- `f1_score(y_test, y_pred)`:
    media armonica de precision y recall.
    penaliza cuando una de las dos es baja.
- `roc_auc_score(y_test, y_proba)`:
    requiere probabilidades (no etiquetas 0/1).
    mide que tan bien ordena positivos por encima de negativos en distintos umbrales.

### 6.4 Mostrar resultados por consola

```python
print(f"Accuracy : {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall   : {recall:.3f}")
print(f"F1-Score : {f1:.3f}")
print(f"ROC-AUC  : {roc_auc:.3f}")
```

- cada `print(...)` muestra la metrica ya calculada.
- `f"...{variable:.3f}"`:
    formatea el numero con 3 decimales.
    ejemplo: `0.81234` se muestra como `0.812`.
- si quieres porcentaje, puedes usar `*100` y agregar `%`.
    ejemplo: `print(f"Accuracy : {accuracy*100:.2f}%")`.

### 6.5 Matriz de confusion (valores exactos de aciertos/errores)

```python
cm = confusion_matrix(y_test, y_pred)
print(cm)
```

- `confusion_matrix(y_test, y_pred)`:
    construye matriz `2x2` (binaria) con estructura:

    `[[TN, FP],`
    ` [FN, TP]]`

- `print(cm)`:
    imprime los conteos reales para analizar en que se equivoca el modelo.

### 6.6 Reporte detallado por clase

```python
print(classification_report(y_test, y_pred, target_names=["Baja calidad (0)", "Alta calidad (1)"]))
```

- `classification_report(...)`:
    genera tabla con precision, recall, f1-score y soporte para cada clase.
- `target_names=[...]`:
    reemplaza etiquetas numericas (`0`, `1`) por nombres legibles.
- `support` en el reporte:
    indica cuantas muestras reales hay de cada clase en `y_test`.

### 6.7 Grafica de matriz de confusion

```python
ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Baja", "Alta"]).plot(cmap="Blues")
plt.title("Matriz de confusion - Gradient Boosting")
plt.show()
```

- `ConfusionMatrixDisplay(...).plot(...)`:
    dibuja la matriz como mapa de calor.
- `display_labels=["Baja", "Alta"]`:
    etiquetas visuales para filas/columnas.
- `cmap="Blues"`:
    define paleta de colores (mas oscuro = mayor conteo).
- `plt.title(...)`:
    agrega titulo a la figura.
- `plt.show()`:
    renderiza el grafico en el notebook.

### 6.8 Resumen de flujo completo

1. el modelo predice etiquetas (`y_pred`) y probabilidades (`y_proba`).
2. con etiquetas calculas accuracy, precision, recall y f1.
3. con probabilidades calculas ROC-AUC.
4. con etiquetas construyes matriz de confusion y reporte por clase.
5. finalmente visualizas la matriz para interpretar errores rapidamente.

### 6.9 Errores comunes y como evitarlos

- usar `roc_auc_score(y_test, y_pred)` en vez de probabilidades:
    funciona, pero pierde informacion. mejor `y_proba`.
- confusion de orden en argumentos:
    siempre usa `metrica(y_real, y_pred)`.
- interpretar mal la matriz:
    recuerda formato `[[TN, FP], [FN, TP]]`.
- mezclar escalas en informe:
    decide si reportas en `0-1` o en `%` y mantenlo consistente.




