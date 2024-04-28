# OrderFy

Gestion de pedidos presencial en restoranes, bares, etc

## Requisitos

- Python 3.x
- Pip

## Instalación

1. Clona este repositorio en tu máquina local.
2. Crea un entorno virtual para el proyecto (opcional pero recomendado).
3. Instala las dependencias del proyecto usando el archivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Tareas de cada uno 

Hugo:
- Hacer todo el front 

Alejo:
- Hacer el sistema de pedidos
  - Ver como hacer para que el pedido llegue a la cocina (mesas?, ajax?) <br>
  - Poner info del menu item en el template de add_item_order (imagen, descripcion, etc.) <br>
- Hacer el sistema de pago <br>
  - Dar la opcion de elegir al restoran si el cliente puede pagar antes o despues, o los dos <br>
- Hacer paginas para los errores (btn logout) <br>
- Ver como agregar la opcion de promos <br>
- Acomodar bien el sistema de permisos especiales por usuario?<br>


Opcionales Alejo:
- Pensar bien si las relaciones de tablas estan bien (el usuario tendria que crear un menu item y una category igual por cada sucursal si el menu es el mismo) <br>
- Agregar bien el window.focus automatico y poner que al tocar enter te toque el boton submit o pase al siguiente input (depende de donde tocas enter) <br>
- Que se recarguen en tiempo real los pedidos en el orders de la cocina <br>


Cualquiera:
- Averiguar sobre como hacer para adaptarse a lo que ya vienen usando los restoranes (la idea es que usen el nuestro desde 0, pero alguno no van a querer)
- Averiguar sobre como subir la pagina


## Créditos

Este proyecto fue creado por Alejo Carranza y Hugo Diaz Otañez.

## Licencia

Este proyecto está bajo la Licencia 'OrderFy'.