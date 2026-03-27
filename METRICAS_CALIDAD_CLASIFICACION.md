# Teoría de Métricas de Calidad en Clasificación

## Introducción

Las métricas de calidad son medidas numéricas fundamentales para evaluar el desempeño de un modelo de clasificación. A diferencia del **accuracy** (exactitud), que puede ser engañoso cuando las clases están desbalanceadas, estas métricas proporcionan una visión más completa y confiable del rendimiento real del modelo.

### Matriz de Confusión: Conceptos Base

Antes de profundizar en cada métrica, es esencial entender los cuatro conceptos fundamentales que forman la base de todas las métricas:

- **TP (True Positives - Verdaderos Positivos)**: El modelo predijo la clase positiva (1) y efectivamente era positiva.
- **TN (True Negatives - Verdaderos Negativos)**: El modelo predijo la clase negativa (0) y efectivamente era negativa.
- **FP (False Positives - Falsos Positivos)**: El modelo predijo la clase positiva (1) pero era negativa.
- **FN (False Negatives - Falsos Negativos)**: El modelo predijo la clase negativa (0) pero era positiva.

Estos cuatro valores forman una tabla llamada **matriz de confusión**:

```
                Predicción Positiva    Predicción Negativa
Clase Real 1         TP                      FN
Clase Real 0         FP                      TN
```

---

## 1. Accuracy (Exactitud)

### Definición

La exactitud es la proporción total de predicciones correctas respecto al total de muestras. Es la métrica más intuitiva, pero puede ser engañosa cuando hay desbalance de clases.

### Fórmula

$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$

### Interpretación

- **Rango**: 0 a 1 (o 0% a 100%)
- **Interpretación**: Porcentaje general de predicciones correctas
- **Ejemplo**: Si accuracy = 0.92, significa que el modelo acertó el 92% de sus predicciones

### Cuándo Usarla

- ✅ Cuando las clases están balanceadas
- ✅ Para obtener una visión general rápida
- ❌ Cuando hay desbalance significativo de clases
- ❌ Cuando los costos de error varían según el tipo

### Limitación Importante

**Ejemplo del problema**: Supón que tienes 100 vinos, de los cuales 95 son de baja calidad y 5 de alta calidad. Si tu modelo simplemente predice "baja calidad" para todo:
- Accuracy = 95/100 = 95% ✓ (parece excelente)
- Pero detecta 0 vinos de alta calidad (FRACASO total para la clase relevante)

---

## 2. Precision (Precisión)

### Definición

La precisión responde a la pregunta: **"De todo lo que el modelo predijo como positivo, cuánto era realmente positivo?"** Mide la confiabilidad de las predicciones positivas.

### Fórmula

$$\text{Precision} = \frac{TP}{TP + FP}$$

### Interpretación

- **Rango**: 0 a 1
- **Interpretación**: De cada 10 predicciones positivas, ¿cuántas son correctas?
- **Ejemplo**: Si precision = 0.85, significa que el 85% de los vinos que predijo como "alta calidad" realmente lo son

### Cuándo Usarla

- ✅ Cuando quieres **evitar falsos positivos** (errores costosos)
- ✅ En detección de spam: No quieres marcar emails válidos como spam
- ✅ En diagnóstico de enfermedades graves: No quieres alarmar falsamente al paciente
- ✅ En sistemas de crédito: No quieres aprobar a clientes malos

### Ejemplo Práctico

Si un banco usa un modelo para detectar fraude:
- Precision alta = Pocas alertas falsas (menos clientes molestos)
- Precision baja = Muchas alertas falsas (pérdida de confianza de clientes)

---

## 3. Recall (Sensibilidad/Cobertura)

### Definición

El recall responde a: **"De todos los casos positivos reales, cuántos detectó el modelo?"** Mide la capacidad de no pasar por alto los casos positivos.

### Fórmula

$$\text{Recall} = \frac{TP}{TP + FN}$$

### Interpretación

- **Rango**: 0 a 1
- **Interpretación**: ¿Qué porcentaje de los positivos reales logró detectar?
- **Ejemplo**: Si recall = 0.90, significa que el modelo detectó el 90% de los vinos de alta calidad

### Cuándo Usarla

- ✅ Cuando quieres **evitar falsos negativos** (ignorar casos positivos importantes)
- ✅ En detección de enfermedades: No quieres dejar pasar pacientes enfermos
- ✅ En control de calidad: No quieres que pasen productos defectuosos
- ✅ En búsqueda y rescate: No puedes dejar de encontrar a alguien

### Ejemplo Práctico

Si un hospital usa un modelo para diagnosticar cáncer:
- Recall alto = Detecta casi todos los casos de cáncer (pocos falsos negativos)
- Recall bajo = Deja pasar muchos casos de cáncer (PELIGROSO)

---

## 4. Trade-off Precision vs Recall

### El Dilema

Es frecuente que aumentar precision disminuya recall y viceversa. Esto es porque:

- **Aumentar umbral de confianza**: Detecta menos positivos (recall ↓) pero los que detecta son más confiables (precision ↑)
- **Disminuir umbral de confianza**: Detecta más positivos (recall ↑) pero comete más errores (precision ↓)

### Visualización Mental

```
Modelo Conservador (Precision ↑, Recall ↓):
- Solo predice "positivo" si está muy seguro
- Pocos falsos positivos, muchos falsos negativos

Modelo Agresivo (Recall ↑, Precision ↓):
- Predice "positivo" fácilmente
- Muchos falsos positivos, pocos falsos negativos
```

---

## 5. F1-Score

### Definición

El F1-Score es la **media armónica** entre precision y recall. Es una métrica que combina ambas métricas en un único valor balanceado, diseñada específicamente para penalizar a modelos que son excelentes en una métrica pero desastrosos en la otra.

#### ¿Por qué es importante?

Imagina dos modelos extremos:

**Modelo A (Conservador):**
- Precision = 95% (cuando predice positivo, acierta el 95% de las veces)
- Recall = 5% (pero solo detecta el 5% de los casos positivos reales)
- **¿Vale la pena?** NO. De qué sirve estar 95% seguro si solo detectas 1 de cada 20 casos positivos

**Modelo B (Agresivo):**
- Precision = 5% (cuando predice positivo, acierta solo el 5% de las veces)
- Recall = 95% (detecta el 95% de los casos positivos reales)
- **¿Vale la pena?** NO. Detectas casi todo, pero generas 95 falsas alarmas por cada 100 predicciones positivas

**F1-Score penaliza fuertemente ambos casos** porque:

1. **No puedes sacrificar una métrica por otra**: A diferencia de usar precision O recall por separado, F1-Score te obliga a tener un buen desempeño en AMBAS. Un modelo verdaderamente bueno debe tener AMBAS métricas altas.

2. **Penaliza desproporcionadamente el desbalance extremo**: Si una métrica es muy alta y la otra muy baja, F1-Score baja significativamente, alertándote de que tu modelo tiene un "punto débil fatal". Por ejemplo, con Precision = 1.0 (perfecto) pero Recall = 0.1 (terrible), F1-Score = 0.18 (muy bajo), te dice claramente: "algo anda muy mal".

3. **Ideal cuando los errores tienen costos similares**: F1-Score es mejor cuando tanto los falsos positivos como los falsos negativos son igualmente problemáticos. Si uno cuesta significativamente más que el otro, deberías usar una métrica diferente o ajustar manualmente los pesos en el modelo.

#### Ejemplo Numérico: Cómo F1-Score Castiga la Debilidad

Compara estos 4 modelos:

| Modelo | Precision | Recall | Media Aritmética | **F1-Score** | ¿Cuál es mejor? |
|--------|-----------|--------|------------------|-----|---|
| **Modelo 1** (Equilibrado) | 80% | 80% | 80% | **80%** | ✅ BUENO - Ambas métricas altas |
| **Modelo 2** (Conservador) | 95% | 10% | 52.5% | **17.8%** | ❌ MALO - La media aritmética oculta el desastre |
| **Modelo 3** (Agresivo) | 10% | 95% | 52.5% | **17.8%** | ❌ MALO - Igual problema |
| **Modelo 4** (Mediocre) | 50% | 50% | 50% | **50%** | ⚠️ PEOR - Verdaderamente mediocre |

**Lo crucial:** Observa los Modelos 2 y 3. La media aritmética = 52.5%, mientras que **F1-Score = 17.8%**. F1-Score "castiga" mucho más fuertemente porque dice: *"No importa si eres perfecto en un lado si fracasas completamente en el otro"*.

**En resumen:** F1-Score es un **"árbitro justo"** que no permite que un modelo escape de su debilidad siendo excelente en otra parte. Obliga al modelo a ser "redondo" (bueno en ambas dimensiones). **Si tu Precision y Recall no están cercanos, tu F1-Score será bajo, alertándote del problema.**

### Fórmula

$$\text{F1-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

También puede expresarse como:

$$\text{F1-Score} = \frac{2 \times TP}{2 \times TP + FP + FN}$$

### ¿Por qué "Media Armónica"?

La media armónica es más restrictiva que la media aritmética. Penaliza desproporcionadamente cuando una métrica es muy baja:

- Si Precision = 1.0 y Recall = 0.1:
  - Media aritmética = (1.0 + 0.1) / 2 = 0.55
  - F1-Score = 2 × (1.0 × 0.1) / (1.0 + 0.1) = **0.18** (mucho más bajo)

### Interpretación

- **Rango**: 0 a 1
- **Interpretación**: Balance general entre precision y recall
- **Ejemplo**: Si F1 = 0.82, indica un buen equilibrio entre detectar positivos y confiar en esas detecciones

### Cuándo Usarla

- ✅ **Recomendada cuando hay desbalance de clases**
- ✅ Cuando necesitas un balance entre precision y recall
- ✅ Cuando quieres un único número para comparar modelos
- ✅ En problemas donde falsos positivos y falsos negativos tienen costo similar

---

## 6. ROC-AUC (Receiver Operating Characteristic - Area Under the Curve)

### Definición

ROC-AUC mide la **capacidad del modelo para separar las dos clases** variando el umbral de decisión. El AUC es el área bajo la curva ROC, que va de 0 a 1.

### ¿Cómo se calcula?

La curva ROC grafica:
- **Eje X (FPR)**: Tasa de Falsos Positivos = $\frac{FP}{FP + TN}$ (¿Cuántos negativos clasificó mal?)
- **Eje Y (TPR)**: Tasa de Verdaderos Positivos = $\frac{TP}{TP + FN}$ (= Recall, ¿Cuántos positivos detectó?)

La curva se genera variando el umbral de decisión de 0 a 1, y el AUC es el área bajo esa curva.

### Fórmula del AUC

$$\text{AUC} = \int_0^1 \text{TPR}(t) \, dt$$

donde $t$ es el umbral de decisión.

### Interpretación

| AUC | Significado |
|-----|-------------|
| 0.5 | El modelo es **tan bueno como lanzar una moneda** (no separación) |
| 0.7 - 0.8 | **Discriminación aceptable** |
| 0.8 - 0.9 | **Discriminación excelente** |
| 0.9 - 1.0 | **Discriminación extraordinaria** |
| 1.0 | **Separación perfecta** (caso ideal) |

### Ventajas

- ✅ **Insensible al desbalance de clases**: No se ve afectado por proporción de clases
- ✅ **Evalúa probabilidades**: Usa `predict_proba`, no solo predicciones discretas
- ✅ **Comparación robusta**: Excelente para comparar diferentes modelos
- ✅ **Resumen único**: Un solo número que resume la performance completa

### Caso de Uso

Es la métrica más robusta para comparar modelos binarios, especialmente con datos desbalanceados.

---

## 7. Matriz de Confusión (Confusion Matrix)

### Definición

La matriz de confusión es una **tabla que presenta visualmente todos los tipos de predicciones**. Con ella puedes ver exactamente dónde y cómo falla el modelo.

### Estructura de la Matriz

Para clasificación binaria:

$$\begin{bmatrix} 
TN & FP \\
FN & TP 
\end{bmatrix}$$

O de forma más descriptiva:

```
                        Predicción = 0    Predicción = 1
Valor Real = 0              TN                FP
Valor Real = 1              FN                TP
```

### Ejemplo Numérico

Supón que evaluaste 200 vinos:

```
                        Predijo Baja (0)    Predijo Alta (1)
Realmente Baja (0)          125                 15
Realmente Alta (1)           8                  52
```

**Interpretación**:
- **TN = 125**: 125 vinos de baja calidad correctamente identificados
- **FP = 15**: 15 vinos de baja calidad incorrectamente etiquetados como alta (error tipo 1)
- **FN = 8**: 8 vinos de alta calidad no detectados (error tipo 2)
- **TP = 52**: 52 vinos de alta calidad correctamente detectados

### Cálculo de métricas a partir de la matriz

$$\text{Accuracy} = \frac{125 + 52}{200} = 88.5\%$$

$$\text{Precision} = \frac{52}{52 + 15} = 77.6\%$$

$$\text{Recall} = \frac{52}{52 + 8} = 86.7\%$$

$$\text{F1-Score} = 2 \times \frac{0.776 \times 0.867}{0.776 + 0.867} = 81.9\%$$

### Ventajas de la Matriz de Confusión

- ✅ **Visualización clara**: Ves exactamente qué tipos de errores comete
- ✅ **Base para otras métricas**: Todas las métricas se derivan de ella
- ✅ **Análisis profundo**: Puedes detectar patrones de error
- ✅ **Comunicación**: Fácil de explicar a stakeholders
