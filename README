# Proyecto de Gramática CFG con Conversión a CNF y Algoritmo CYK

Este proyecto implementa la conversión de una gramática libre de contexto (CFG) a su Forma Normal de Chomsky (CNF) y utiliza el algoritmo CYK (Cocke-Younger-Kasami) para determinar si una oración pertenece al lenguaje descrito por la gramática. También genera el árbol de análisis (parse tree) de la oración, en caso de que pertenezca al lenguaje.

## Estructura del Proyecto

El proyecto sigue la arquitectura MVC (Modelo-Vista-Controlador) para mantener un código organizado y fácilmente mantenible. A continuación, se detalla cómo se define la gramática y cómo se procesa.

### Definición de la Gramática (Ejemplo)

La gramática se representa como un objeto de Python en formato JSON que contiene:
- **Variables (No terminales)**: Los símbolos que representan agrupaciones de otras reglas.
- **Terminales**: Los símbolos finales del lenguaje (palabras o tokens).
- **Reglas**: Las reglas que indican cómo se pueden combinar las variables y terminales.

Un ejemplo de gramática libre de contexto (CFG) sería:

```python
grammar_data = {
    "variables": ["S", "NP", "VP"],
    "terminals": ["he", "she", "drinks", "a", "beer"],
    "rules": [
        {"S": ["NP VP"]},
        {"NP": ["he", "she"]},
        {"VP": ["drinks NP"]},
        {"NP": ["a beer"]}
    ]
}
```