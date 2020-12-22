from datetime import datetime,timedelta
import heapq

class Convertidor:

	@staticmethod
	def parsear_entrada(aeropuerto:str):
		return aeropuerto.upper()

	@staticmethod
	def diferencia_horaria(hora1:str , hora2:str):
		""" Recibe dos horarios y calcula el lapso entre ellas
			Retorna el tiempo transcurrido entre dos horas en formato horas:minutos
		"""
		formato = "%H:%M"
		delta = datetime.strptime(hora2,formato) - datetime.strptime(hora1,formato)
		if delta.days < 0:
			delta = timedelta(days=0,seconds=delta.seconds,microseconds=delta.microseconds)
		return delta
	
	@staticmethod
	def total_minutos(tiempo:str):
		""" Recibe un formato de horas y minutos y retorna la cantidad total de minutos"""
		return tiempo.total_seconds() / 60
	
	@staticmethod
	def formatear_total_horas(minutos:float):
		""" Recibe la cantidad de minutos y retorna la cantidad de horas que conforman esos minutos 
		en el formato horas:minutos:segundos"""
		minutos = timedelta(minutes=minutos)
		return str(minutos)


class Arista:

	def __init__(self,origen,destino,costo_tiempo,costo_dinero):
		self.origen = origen #i
		self.destino = destino #j
		self.tiempo = costo_tiempo #tiempo de ir de origen->destino
		self.dinero = costo_dinero #dinero de ir de origen->destino

	def __str__(self):
		fuente = f"desde: {self.origen} -> hacia {self.destino}:=  "
		costos = f"tiempo: {self.tiempo} , precio viaje: {self.dinero}"
		return fuente + costos


class Grafo:
	inf = 99999999 #representacion de INFINITO

	def __init__(self,num_nodos:int,identificadores:dict):

		self.numNodos = num_nodos #numero de nodos del grafo
		self.ids = identificadores #tabla para convetir id numerico en id de caracteres map
		self.grafo = [[] for nodo in range(self.numNodos)] #Lista de adyacencia
	

	def crear_arista(self,desde:int,hacia:int,tiempo:str,precio:int):
		vecino = Arista(desde,hacia,tiempo,precio) #crear una nueva arista
		self.grafo[desde].append(vecino) #ingresar arista a la lista de lista


	def mostrarGrafo(self):
		for i in range(self.numNodos):
			for j in range(len(self.grafo[i])):
				print("{} -> {}".format(self.ids[self.grafo[i][j].origen],self.ids[self.grafo[i][j].destino]))


	#metodo privado para mostrar el camino que requiere menos escalas
	def __construir_camino_con_menos_escalas(self,origen,destino,padres,camino=[]):
		camino.append(destino)
		while destino in padres:
			destino = padres[destino]

			#evitar un padre no existente en el grafo real
			if destino not in padres:
				destino = camino[0] #ya que cuando es un -1 , nos quedamos con el nodo destino , en vez del -1
				break

			camino.append(destino)
		camino.reverse()

		print("")
		if len(camino) == 1: #es porque solo esta el nodo origen y no existe un destino
			print(f"No existe ruta desde {self.ids[origen]} hasta {self.ids[destino]}")
		else:
			print(f"La ruta con menos escalas desde {self.ids[origen]} hacia {self.ids[destino]} tiene {len(camino)-2} escalas:")

			for contador,nodo in enumerate(camino):
				if contador == len(camino)-1: #si es el ultimo nodo imprime un salto de linea
					print(f"{self.ids[nodo]}")
				else:
					print(f"{self.ids[nodo]}",end=" -> ")
		print("")


	def vuelo_con_menos_escalas(self,origen,destino):
		""" BFS para hallar el vuelo con menos escalas sin importar el costo ni el tiempo """
		parent = {}
		parent[origen] = -1

		visitados = [False for nodo in range(self.numNodos)]
		visitados[origen] = True

		queue = []
		queue.append(origen)

		while queue:
			nodo_actual = queue.pop(0) #procesamos el nodo actual de la queue

			for vecino in self.grafo[nodo_actual]: #recorrer todos los nodos adyacentes al nodo en proceso
				idVecino = vecino.destino
		
				if not visitados[idVecino]:
					visitados[idVecino] = True
					queue.append(idVecino)
					parent[idVecino] = nodo_actual

					if idVecino == destino:
						break

		self.__construir_camino_con_menos_escalas(origen,destino,parent)


	def vuelo_mas_barato(self,source,target):
		prev = [0 for nodo in range(self.numNodos)]
		prev[source] = -1 #nodo de partida no tiene un padre
		distancias = [self.inf for nodo in range(self.numNodos)]
		distancias[source] = 0 #distancia a si mismo es cero

		pq = [] #crear cola de prioridad

		secuencia = [] #secuencia con el camino minimo desde source hasta target , pendiente: retornar S.reverse() 

		#pushear nodo de partida con (distancia al nodo , id del nodo)
		heapq.heappush(pq , (0,source))

		while pq:
			nodo_actual = heapq.heappop(pq) #extraer el nodo con la distancia minima
			origen = nodo_actual[1]

			#en este segmento devuelve el camino minimo hasta cuando encuentra el nodo destino
			objetivo = target
			if origen == objetivo:
				if prev[objetivo] != -1 or objetivo == source:
					while objetivo != -1:
						secuencia.append(objetivo)
						objetivo = prev[objetivo]

			for nodo in self.grafo[origen]:
				nueva_distancia = distancias[nodo.origen] + nodo.dinero

				if nueva_distancia < distancias[nodo.destino]:
					distancias[nodo.destino] = nueva_distancia
					prev[nodo.destino] = origen
					heapq.heappush(pq , (nodo.dinero , nodo.destino))

		secuencia = setear_secuencia(secuencia)
		secuencia.reverse()
		print("")
		if not secuencia:
			print(f"No existe ruta desde {self.ids[source]} hasta {self.ids[target]}")
		else:
			print(f"La ruta mas barata desde {self.ids[source]} hasta {self.ids[target]} es: ")
			for iterador,nodo in enumerate(secuencia):
				if iterador == len(secuencia) - 1: #imprime salto de linea
					print(f"{self.ids[nodo]}")
				else:
					print(f"{self.ids[nodo]} " , end= "-> ")
			print(f"Costo de la ruta es: ${distancias[target]}")
		print("")
	
	
	def vuelo_con_menos_tiempo(self,source,target):
		tiempos = [self.inf for nodo in range(self.numNodos)]
		prev = [0 for nodo in range(self.numNodos)]

		prev[source] = -1
		tiempos[source] = 0.0

		secuencia = []
		pq = [] #cola de prioridad

		heapq.heappush(pq , (0.0 , source)) #el tiempo de ir de source a source es 0 minutos
		while pq:
			nodo_actual = heapq.heappop(pq)
			origen = nodo_actual[1] #es el id desde donde parte la arista
			
			#en este segmento devuelve el camino minimo hasta cuando encuentra el nodo destino
			objetivo = target
			if origen == objetivo:
				if prev[objetivo] != -1 or objetivo == source:
					while objetivo != -1:
						secuencia.append(objetivo)
						objetivo = prev[objetivo]

			#Parte a modificar para usarla con tiempos en vez de costos
			for nodo in self.grafo[origen]:
				nuevo_tiempo = tiempos[nodo.origen] + Convertidor.total_minutos(nodo.tiempo)

				if nuevo_tiempo < tiempos[nodo.destino]:
					tiempos[nodo.destino] = nuevo_tiempo
					prev[nodo.destino] = origen
					heapq.heappush(pq , (nodo.tiempo , nodo.destino))

		secuencia = setear_secuencia(secuencia)
		secuencia.reverse()
		print("")
		if not secuencia:
			print(f"No existe ruta desde {self.ids[source]} hasta {self.ids[target]}")
		else:
			print(f"La ruta con menos tiempo desde {self.ids[source]} hasta {self.ids[target]} es: ")
			for iterador,nodo in enumerate(secuencia):
				if iterador == len(secuencia) - 1: #imprime salto de linea
					print(f"{self.ids[nodo]}")
				else:
					print(f"{self.ids[nodo]} " , end= "-> ")
			tiempo_total = Convertidor.formatear_total_horas(tiempos[target])
			print(f"Tiempo de la ruta es: {tiempo_total}")
		print("")

#----------------------------------- Fin Clases -------------------------------------------------------
def setear_secuencia(secuencia):
	result = set()
	nueva_secuencia = []
	for item in secuencia:
		if item not in result:
			result.add(item)
			nueva_secuencia.append(item)
	return nueva_secuencia

def main():
	tabla_nombres = dict()
	identificadores = dict()

	aristas = []

	#Leer itinerario como fichero de texto
	NOMBRE_FICHERO = "itinerario.txt"
	with open(NOMBRE_FICHERO,'r') as file:
		numVuelos = int(file.readline())
		contador = 0

		for i in range(0,numVuelos):
			infoVuelo = file.readline().strip()
			infoVuelo = infoVuelo.split(' ')
			origen,destino,hora_salida,hora_llegada,precio = infoVuelo
			precio = int(precio.split('$')[1])

			info = (origen,destino,hora_salida,hora_llegada,precio)
			aristas.append(info)

			#mapear nombres a numeros y viceversa
			#origen = Convertidor.parsear_entrada(origen)
			#destino = Convertidor.parsear_entrada(destino)

			if origen not in tabla_nombres:
				tabla_nombres[origen] = contador
				identificadores[contador] = origen
				contador += 1
			if destino not in tabla_nombres:
				tabla_nombres[destino] = contador
				identificadores[contador] = destino
				contador += 1

		num_nodos = len(identificadores)
		grafo = Grafo(num_nodos,identificadores)

		for arista in aristas:
			desde = tabla_nombres[arista[0]]
			hacia = tabla_nombres[arista[1]]
			tiempo = Convertidor.diferencia_horaria(arista[2],arista[3])
			precio = arista[4]
			grafo.crear_arista(desde,hacia,tiempo,precio)


	#Consultar itinerario de vuelo	
	origen = str(input("Ingrese origen: "))
	destino = str(input("Ingrese destino: "))

	#convertir a mayusculas
	origen = Convertidor.parsear_entrada(origen)
	destino = Convertidor.parsear_entrada(destino)

	#Verificar que las nombres esten bien ingresados
	while origen not in tabla_nombres:
		print(f"Aeropuerto {origen} no existe,ingreselo nuevamente")
		origen = str(input("Ingrese origen: "))
		origen = Convertidor.parsear_entrada(origen)
	while destino not in tabla_nombres:
		print(f"Aeropuerto {destino} no existe,ingreselo nuevamente")
		destino = str(input("Ingrese destino: "))
		destino = Convertidor.parsear_entrada(destino)

	#convetir nombre a identificador numerico
	origen = tabla_nombres[origen]
	destino = tabla_nombres[destino]

	#Camino con menos escalas , sin importar costos ni tiempos
	grafo.vuelo_con_menos_escalas(origen,destino)
	
	#vuelo_mas_barato retorna las distancias y los padres hasta el nodo destino
	grafo.vuelo_mas_barato(origen,destino)

	#vuelo con menos tiempo
	grafo.vuelo_con_menos_tiempo(origen,destino)

if __name__ == '__main__':
	main()
