# Professional Tennis Game

Un juego de tenis profesional desarrollado con Pygame que incluye sprites de jugadores humanos, reglas de tenis apropiadas y un menú profesional.

## Características

- **Sprites de Jugadores**: Jugadores representados como personas con cabeza, cuerpo y raqueta
- **Reglas de Tenis Apropiadas**: Sistema de puntuación completo (0, 15, 30, 40, deuce, advantage)
- **Menú Profesional**: Interfaz de usuario con navegación completa
- **Física Realista**: Movimiento de pelota con gravedad y resistencia del aire
- **Estados de Juego**: Menú, jugando, pausado, game over
- **Cancha Detallada**: Cancha de tenis con líneas de servicio y red

## Controles

### Jugador 1 (Azul)
- **WASD**: Movimiento
- **Espacio**: Golpear la pelota

### Jugador 2 (Rojo)
- **Flechas**: Movimiento
- **Espacio**: Golpear la pelota

### Controles Generales
- **ESC**: Pausar/Reanudar el juego
- **Mouse**: Navegación del menú

## Reglas del Tenis

1. **Puntuación**: 0, 15, 30, 40, Juego
2. **Deuce**: Cuando ambos jugadores tienen 40 puntos
3. **Advantage**: Ventaja después del deuce
4. **Games**: Primero en ganar 6 juegos con ventaja de 2
5. **Sets**: Primero en ganar 2 sets gana el partido

## Instalación y Ejecución

### Requisitos
- Python 3.x
- pygame
- numpy

### Ejecutar el juego
```bash
python3 tennis_game.py
```

## Estructura del Proyecto

- `tennis_game.py`: Archivo principal del juego
- `requirements.txt`: Dependencias del proyecto
- `README.md`: Este archivo

## Características Técnicas

- **Resolución**: 1200x800 píxeles
- **FPS**: 60 frames por segundo
- **Física**: Simulación realista de movimiento de pelota
- **Gráficos**: Renderizado en tiempo real con efectos visuales

¡Disfruta jugando tennis profesional!