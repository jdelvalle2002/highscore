# Highscore
*Intentando recrear el juego de ravensburger "highscore" en Python*

*Update: objetivo logrado*


El archivo principal es `highscore-multicovaPOO.py`. Teniendo ese archivo y Python con las librerías necesarias ya puedes jugar... Y en multijugador!!!

¡Actualmente también hay una versión disponible sin necesidad de Python! Para ello ir a la sección de [releases](https://github.com/jdelvalle2002/highscore/releases). Ahí encontrarás versiones `.exe`,`.app` y para Linux. Si quieres revisar el código fuente para estas versiones puedes revisar la carpeta `release3` del repositorio. En la carpeta `highscore` puedes encontrar versiones primitivas del juego y residuos varios.

Puedes encontrar también toda esta información en el [sitio web creado para el juego](https://highscore-on-python.netlify.app/).
## ¿En qué consiste?

Para el juego necesitas un tablero de 5x5, dos dados y un lápiz (tranqui, todos están "incluidos").
Cada ronda se lanzan los dados, y el número que sale debe ser anotado en el tablero, intentando formar combinaciones con los números en la correspondiente columna, fila, o diagonal.

Una vez lanzados los dados de la siguiente ronda no se puede alterar el número escrito.

Las combinaciones tienen los siguientes puntajes:
- Par: 1 punto
- 2 pares: 3 puntos
- Trio: 3 puntos
- Poker: 6 puntos
- Quinteto: 10 puntos
- Full: 8 puntos
- Escala con 7: 8 puntos
- Escala sin 7*: 12 puntos

**Las diagonales suman el doble de puntos**        

(*) *Las escalas sin 7 tienen más puntaje porque el 7 tiene más probabilidades de salir, entonces es más difícil construir una escala de esas características.*

Cuando se termian de rellenar el tablero se cuentan los puntos totales, el mayor puntaje gana.

[Acá puedes aprender más del juego (si sabes holandés...)](https://www.libble.eu/ravensburger-high-score/c582698/)



Requiere la instalación de la libreria `tkinter` y `webbrowser` (probablemente ya las tienes).


