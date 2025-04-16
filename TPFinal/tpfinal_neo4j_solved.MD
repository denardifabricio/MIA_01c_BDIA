<img src="https://github.com/hernancontigiani/ceia_memorias_especializacion/raw/master/Figures/logoFIUBA.jpg" alt="logoFIUBA" width="600">

# Trabajo Práctico Final
Finalmente, desarrollé el TP final propuesto por la cátedra. \
Se nos propuso a los alumnos elegir entre los tipos diferentes de base de datos vistos. 

# Consigna
Ver [Grafos.pdf](Grafos.pdf) con la propuesta.

# Motivación
Elegí el orientado a grafos, pues me pareció el más interesante y distinto a lo que yo estaba acostumbrado a ver en mi carrera profesional. El de SQL no me aportaba valor y el de nodejs es algo que muy facilmente con tutoriales se puede aprender o implementar profesionalmente sin mayores sobresaltos, en cambio el de grafo lo veo más orientados a problemas de ML, de hecho este tp es una aproximación a un problema real.

# Prerequisitos y comentarios previos

## PaySim
El detalle completo de la implementación de este simulador de transacciones financieras se puede ver en el [link](https://www.sisu.io/posts/paysim-part2/) descripto en la consulta.

A modo de resumen, la siguiente imagen representa el modelo de datos sobre el que se trabajará:
<img src="img/paysim-2.1.0.png" alt="nodos" >

### Instalación
Se siguieron los pasos para instalar de acuerdo al [repo](https://github.com/voutilad/paysim-demo) suguerido en la página del simulador.

#### Problemas durante la instalación
1. En primer lugar tuve problemas con la versión de JDK de Java. En mi laptop tenía instalada la última versión y el script solo soloporta 8 y 11, al parecer java no es retrocompatible, o por lo menos entre las versiones mencionadas.

2. El script por defecto exige un puerto y password determinado, al principio no había respetado esto entonces no creaba nada en ninguna db.

Finalmente logré que funcione:

Para chequear que se haya importado, realicé una consulta suguerida también en la página del simulador, en donde se muestra la frecuencia y frecuencia relativa de los elementos.

```sql
CALL db.labels() YIELD label
CALL apoc.cypher.run('MATCH (:`'+label+'`) RETURN count(*) as freq',{}) YIELD value
WITH label,value.freq AS freq
CALL apoc.meta.stats() YIELD nodeCount
WITH *, 10^3 AS scaleFactor, toFloat(freq)/toFloat(nodeCount) AS relFreq
RETURN label AS nodeLabel,
    freq AS frequency,
    round(relFreq*scaleFactor)/scaleFactor AS relativeFrequency
ORDER BY freq DESC
```
![alt text](img/query_00.png)

Nota: He detectado que hay diferencia entre la cantidad de registros que el proceso local me creó respecto a lo que la imagen del sitio se ve. En este caso asumí que no fue un error del proceso sino que se trata de ejemplos que van variando en el tiempo. Puesto que las queries de ejemplo siguen el mismo orden y guardan simulitud, por ejemplo hay muchas mas transacciones que notas de créditos. 

También hice otra query muy sencilla para ver en formato nodo si respetaba el grafo teórico, cosa que sí lo hizo. La siguiente imagen muestra un fragmento del resultado obtenido:
```sql
MATCH (n)-[r]->(m)
RETURN n, r, m
LIMIT 100
```
![alt text](img/query_00_1.png)
<br/> Se puede observar que los nodos y las relaciones siguen la del gráfico teórico.

# Resolución
A continuación se mostrará la resolución para cada consulta solicitada en la consigna. Basicamente es realizar ejercicios sobre un simulador de transacciones financieras.

## 1. Mercantes con transacciones fraudulentas por más de un cliente 
Identifica los mercantes que tuvieron transacciones fraudulentas con más de un cliente,ordenados en forma descendente por monto total. 

```sql
MATCH (c:Client)-[:PERFORMED]->(t:Transaction {fraud: true})-[:TO]->(m:Merchant)
WITH m, COUNT(DISTINCT c) AS numClientes, SUM(t.amount) AS totalFraudAmount
WHERE numClientes > 1
RETURN m.id AS MerchantID, numClientes AS FraudulentClients, totalFraudAmount AS TotalFraudAmount
ORDER BY totalFraudAmount DESC
```
![alt text](img/query_01.png)

Nota Ejercicio 1: Esta query es la que más tiempo me llevo, no por la complejidad sino porque tuve que investigar los labels, properties, nodes, etc. Es decir el modelo de datos.


## 2. Clientes con información PII compartida 
Encuentra los clientes que comparten información PII (Mail, teléfono o SSN) con más de una persona. Deberás contar cuántas personas comparten información con cada cliente y ordenar de forma descendente. 
```sql
MATCH (c1:Client)
OPTIONAL MATCH (c1)-[:HAS_EMAIL]->(e:Email)<-[:HAS_EMAIL]-(c2:Client)
WHERE c1.id <> c2.id
WITH c1, COLLECT(DISTINCT c2.name) AS sharedEmailClients

OPTIONAL MATCH (c1)-[:HAS_PHONE]->(p:Phone)<-[:HAS_PHONE]-(c3:Client)
WHERE c1.id <> c3.id
WITH c1, sharedEmailClients, COLLECT(DISTINCT c3.name) AS sharedPhoneClients

OPTIONAL MATCH (c1)-[:HAS_SSN]->(s:SSN)<-[:HAS_SSN]-(c4:Client)
WHERE c1.id <> c4.id
WITH c1, 
     sharedEmailClients + sharedPhoneClients AS combinedClients, 
     COLLECT(DISTINCT c4.name) AS sharedSSNClients

WITH c1, combinedClients + sharedSSNClients AS allSharedClients

WITH c1, apoc.coll.toSet(allSharedClients) AS uniqueSharedClients
WHERE SIZE(uniqueSharedClients) > 1
RETURN c1.id AS ClientID, c1.name,  SIZE(uniqueSharedClients) AS SharedPIICount, uniqueSharedClients AS SharedWith
ORDER BY SharedPIICount DESC
```
![alt text](img/query_02.png)

Nota Ejericio 2: Junto con el ejericio 6, esta query me llevó a investigar más, buscando docu y ayudándome de LLMs para su resolución.
Links de referencia: <br/>
https://neo4j.com/docs/cypher-manual/current/clauses/optional-match/ <br/>
https://neo4j.com/docs/cypher-manual/current/clauses/with/ <br/>
https://neo4j.com/docs/cypher-manual/current/functions/scalar/#functions-size



## 3. Cliente con mayor actividad fraudulenta 
Identifica al cliente que ha movido más dinero de manera fraudulenta, ordenado por número de transacciones y monto total en forma descendente. 
```sql
MATCH (c:Client)-[:PERFORMED]->(t:Transaction {fraud: true})
WITH c, COUNT(t) AS numFraudulentTransactions, SUM(t.amount) AS totalFraudAmount
RETURN c.id AS ClientID, c.name, numFraudulentTransactions AS FraudulentTransactions, totalFraudAmount AS TotalFraudAmount
ORDER BY numFraudulentTransactions DESC, totalFraudAmount DESC
LIMIT 1
```
![alt text](img/query_03.png)

Nota ejercicio 3: Vemos que hay un Limit 1, fui jugando con diferentes valores,  lo que quería asegurarme era el orden correcto y que traiga el más grande. Sobre todo cuando coincidía el primer filtro.
![alt text](img/query_03_1.png)

## 4. Banco con más transacciones 
Determina cuál es el banco que ha tenido el mayor número de transacciones. 
```sql
MATCH (t:Transaction)-[:TO]->(b:Bank)
WITH b, COUNT(t) AS numTransactions
RETURN b.id AS BankID, numTransactions AS TotalTransactions
ORDER BY numTransactions DESC
LIMIT 1
```
![alt text](img/query_04.png)

Nota ejercicio 4: Vemos que hay un Limit 1, fui jugando con diferentes valores, no agrego imagen ya que no aporta valor, lo que quería asegurarme era el orden correcto y que traiga el más grande.

## 5. Transferencias fraudulentas a bancos 
Descubre si existen transferencias fraudulentas directas hacia algún banco y cuántas han sido. 
```sql
MATCH (t:Transaction {fraud: true})-[:TO]->(b:Bank)
RETURN b.id AS BankID, COUNT(t) AS FraudulentTransfers
ORDER BY FraudulentTransfers DESC
```
![alt text](img/query_05.png)

Vemos que no hay transacciones fraudlentas directas hacia bancos.

Nota Ejericio 5: Para chequearlo hice la inversa, fraud:false y si me devolvió resultados, como para verificar el correcto funcionameinto de la query. 
Vemos entonces que todos las transacciones directas de banco no son fraudulentas: <br/><br/>
Totales por destino sin discrminiar si son o no fraudelentas: <br/>
![alt text](img/query_05_1.png)
<br/>VS<br/>
Total a bancos no fraudentas:<br/>
![alt text](img/query_05_2.png)

## 6. Camino más corto entre cliente y banco 
Determina cuál es el camino más corto que relaciona al cliente identificado en el ejercicio 3 con el banco determinado en el ejercicio 4. 
```sql
// Encuentra el cliente con mayor actividad fraudulenta y el banco con más transacciones
CALL {
    MATCH (c:Client)-[:PERFORMED]->(t:Transaction {fraud: true})
    WITH c, COUNT(t) AS numFraudulentTransactions, SUM(t.amount) AS totalFraudAmount
    RETURN c.id AS ClientID
    ORDER BY numFraudulentTransactions DESC, totalFraudAmount DESC
    LIMIT 1
} CALL {
    MATCH (t:Transaction)-[:TO]->(b:Bank)
    WITH b, COUNT(t) AS numTransactions
    RETURN b.id AS BankID
    ORDER BY numTransactions DESC
    LIMIT 1
}
// Encuentra el camino más corto entre el cliente y el banco
MATCH (c:Client {id: ClientID}), (b:Bank {id: BankID})
MATCH p = shortestPath((c)-[*]-(b))
RETURN p
```
![alt text](img/query_06.png)
 
 Y también visto como grafo:

 ![alt text](img/query_06_1.png)

Nota Ejercicio 6: La parte que tuve que investigar y valerme de ayudas de LLM fue la de Call, para poder hacerlo dinámico. Porque no quería hardcodear el ClientID ni el BankId.

