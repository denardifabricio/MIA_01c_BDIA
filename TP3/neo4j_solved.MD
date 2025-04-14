<img src="https://github.com/hernancontigiani/ceia_memorias_especializacion/raw/master/Figures/logoFIUBA.jpg" alt="logoFIUBA" width="600">

# Trabajo Práctico Nº 3 orientados a grafos. Neo4j.

# Base de datos 
Ver [Datos_Ejemplo_Neo_formateado.txt](Datos_Ejemplo_Neo_formateado.txt) con la estructura y datos.

# Resolución
A continuación se mostrará la resolución para cada consulta solicitada en la [consigna](TP 3 Bases de grafos.pdf).

## Problema con mac
Tuve un problema con mac, que me abría el archivo dado con los datos de forma errónea. En la carpeta del tp podrá ver un .py donde corregí el fomato, con ayuda de un LLM.

## Formato de respuesta
A fines de mostrar el resultado más legible y que verdaderamente se pueda interpertar una respuesta, el resultado lo mostré en formato .txt.

Por supuesto que habrá queries, como la primera que no se podrá ver el 100% de los datos, se imprimió para ver que el resultado tiene sentido y pude obtenerlo.

### 1. Obtener los nodos de todas las personas de la red.
```js
MATCH (p:Persona)
RETURN p;
```
![alt text](img/query_01.png)


### 2.  Obtener el nombre y fecha de nacimiento de la persona de apellido Domínguez. 
```js
MATCH (p:Persona {apellido: "Dominguez"})
RETURN p.nombre, p.fechanac;
```
![alt text](img/query_02.png)


### 3.  Obtener la lista de empresas en las que trabajó Domínguez.
```js
MATCH (p:Persona {apellido: "Dominguez"})-[:TRABAJO]->(e:Empresa)
RETURN e.nombre AS empresa;
```
![alt text](img/query_03.png)

### 4.  Obtener la lista de personas que estudiaron carreras que no son de nivel “Universitario” y los nombres de las carreras. 
```js
MATCH (p:Persona)-[:ESTUDIO]->(c:Carrera)
WHERE c.nivel <> "Universitario"
RETURN p.nombre AS persona, c.nombre AS carrera;
```
![alt text](img/query_04.png)

### 5.  Obtener los nodos etiquetados como Conocimiento.
```js
MATCH (c:Conocimiento)
RETURN c;
```
![alt text](img/query_05.png)

### 6.  Obtener los nodos de todas las personas con nombre terminado en a.
```js
MATCH (p:Persona)
WHERE p.nombre ENDS WITH "a"
RETURN p;
```
![alt text](img/query_06.png)

### 7.  Crear un nodo para la persona Analía Martinelli si no existe. 
```js
MERGE (p:Persona {nombre: "Analía", apellido: "Martinelli"})
RETURN p;
```
![alt text](img/query_07.png)

### 8.  Asociar un conocimiento "Cálculo" a Analía Martinelli si no lo posee. 
```js
MERGE (c:Conocimiento {nombre: "Cálculo"})
WITH c
MATCH (p:Persona {nombre: "Analía", apellido: "Martinelli"})
MERGE (p)-[:POSEE]->(c)
RETURN p, c;
```
![alt text](img/query_08.png)

### 9.  Verificar si se creó duplicado del conocimiento "Cálculo".
```js
 MATCH (c:Conocimiento {nombre: "Cálculo"})
RETURN COUNT(c) AS total;
```
![alt text](img/query_09.png)


### 10.  Crear una relación ESTUDIO para Analía Martinelli con la carrera "Lic en Sist de Inf", estado "En curso". 
```js
MERGE (c:Conocimiento {nombre: "Cálculo"})
WITH c
MATCH (p:Persona {nombre: "Analía", apellido: "Martinelli"})
MERGE (p)-[:POSEE]->(c)
RETURN p, c;
```
![alt text](img/query_10.png)

### 11. Crear un nodo para Verónica Mendez
```js
CREATE (p:Persona {nombre: "Verónica", apellido: "Mendez"})
RETURN p;
```
![alt text](img/query_11.png)

### 12. Crear una relación CONOCE_A entre Analía y Verónica, asegurando que solo se cree una vez.
```js
MATCH (a:Persona {nombre: "Analía", apellido: "Martinelli"})
MATCH (v:Persona {nombre: "Verónica", apellido: "Mendez"})
MERGE (a)-[:CONOCE_A]->(v)
RETURN a, v;
```
![alt text](img/query_12.png)

### 13. Actualizar o crear el nodo de Analía Martinelli con fecha de nacimiento 30/06/1968.
```js
MATCH (a:Persona {nombre: "Analía", apellido: "Martinelli"})
MATCH (v:Persona {nombre: "Verónica", apellido: "Mendez"})
MERGE (a)-[:CONOCE_A]->(v)
RETURN a, v;
```
![alt text](img/query_13.png)

### 14. Agregarle la etiqueta "Empleado" y el país Argentina a Analía.
```js
MATCH (a:Persona {nombre: "Analía", apellido: "Martinelli"})
MATCH (v:Persona {nombre: "Verónica", apellido: "Mendez"})
MERGE (a)-[:CONOCE_A]->(v)
RETURN a, v;
```
![alt text](img/query_14.png)