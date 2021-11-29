"""
Chapitre 11.2
"""


import numbers
import copy
import collections
import collections.abc


class Matrix:
	"""
	Matrice numérique stockée en tableau 1D en format rangée-major.

	:param height: La hauteur (nb de rangées)
	:param width: La largeur (nb de colonnes)
	:param data: Si une liste, alors les données elles-mêmes (affectées, pas copiées). Si un nombre, alors la valeur de remplissage
	"""

	def __init__(self, height: int, width: int, data: float = 0.0) -> None:
		if not isinstance(height, numbers.Integral) or not isinstance(width, numbers.Integral):
			raise TypeError()
		if height == 0 or width == 0:
			raise ValueError(numbers.Integral)
		self.__height = height
		self.__width = width
		if isinstance(data, list):
			if len(data) != len(self):
				raise ValueError(list)
			self.__data = data
		elif isinstance(data, numbers.Number):
			self.__data = [data for _ in range(len(self))]
		else:
			raise TypeError()

	@property
	def height(self):
		return self.__height

	@property
	def width(self):
		return self.__width

	@property
	def data(self):
		return self.__data

	def __getitem__(self, indexes: tuple) -> float:
		"""
		Indexation rangée-major

		:param indexes: Les index en `tuple` (rangée, colonne)
		"""
		if not isinstance(indexes, tuple):
			raise IndexError()
		if indexes[0] >= self.height or indexes[1] >= self.width:
			raise IndexError()
		
		return self.data[indexes[0] * self.width + indexes[1]]

	def __setitem__(self, indexes: tuple, value: float) -> None:
		"""
		Indexation rangée-major

		:param indexes: Les index en `tuple` (rangée, colonne)
		"""
		if not isinstance(indexes, tuple):
			raise IndexError()
		if indexes[0] >= self.height or indexes[1] >= self.width:
			raise IndexError()
		self.data[indexes[0] * self.width + indexes[1]] = value

	def __len__(self):
		"""
		Nombre total d'éléments
		"""
		return self.height * self.width

	def __str__(self):
		return format(self, "")

	# Représentation officielle
	def __repr__(self):
		# Une string qui représente une expression pour construire l'objet.
		return f"Matrice({self.height}, {self.width}, {self.data.__repr__()})"

	# String formatée
	def __format__(self, format_spec: str):
		# On veut pouvoir dire comment chaque élément doit être formaté en passant la spécification de formatage qu'on passerait à `format()`
		matrix_row = []
		for row in range(self.height):
			values = [format(self[row, index], format_spec) for index in range(self.width)]
			matrix_row.append(" ".join(values))
		
		return "\n".join(matrix_row)


	def clone(self):
		return Matrix(self.height, self.width, self.data)

	def copy(self):
		return Matrix(self.height, self.width, copy.deepcopy(self.data))

	def has_same_dimensions(self, other):
		return (self.height, self.width) == (other.height, other.width)

	def __pos__(self):
		return self.copy()

	# Négation
	def __neg__(self) -> 'Matrix':
		data = []
		for row in range(self.height):
			for index in range(self.width):
				data.append(self[row, index] * -1)

		return Matrix(self.height, self.width, data)

	# Addition
	def __add__(self, other: 'Matrix') -> 'Matrix':
		data = []
		for row in range(self.height):
			for index in range(self.width):
				data.append(self[row, index] + other[row, index])

		return Matrix(self.height, self.width, data)
	
	# Soustraction
	def __sub__(self, other: 'Matrix') -> 'Matrix':
		data = []
		for row in range(self.height):
			for index in range(self.width):
				data = self[row, index] - other[row, index]
		
		return Matrix(self.height, self.width, data)
	
	# Multiplication matricielle/scalaire
	def __mul__(self, other) -> 'Matrix':
		if isinstance(other, Matrix):
			#  Multiplication matricielle.
			# Rappel de l'algorithme simple pour C = A * B, où A, B sont matrices compatibles (hauteur_A = largeur_B)
			# C = Matrice(hauteur_A, largeur_B)
			# Pour i dans [0, hauteur_C[
				# Pour j dans [0, largeur_C[
					# Pour k dans [0, largeur_A[
						# C(i, j) = A(i, k) * B(k, j)
			data = []
			for i in range(self.height):
				for j in range(other.width):
					result = 0
					for k in range(self.width):
						result += self[i, k] * other[k, j]
					data.append(result)

			return Matrix(self.height, other.width, data)

		elif isinstance(other, numbers.Number):
			# Multiplication scalaire.
			data = []
			for row in range(self.height):
				for index in range(self.width):
					data.append(self[row, index] * other)
		
			return Matrix(self.height, self.width, data)

		else:
			raise TypeError()

	# Multiplication scalaire avec le scalaire à gauche
	def __rmul__(self, other: 'Matrix') -> 'Matrix':
		return self * other

	def __abs__(self) -> 'Matrix':
		return Matrix(self.height, self.width, [abs(e) for e in self.data])

	# Égalité entre deux matrices
	def __eq__(self, other: 'Matrix') -> bool:
		return self is other or (self.height, self.width, self.data) == (other.height, other.width, other.data)

	@classmethod
	def identity(cls, width):
		result = cls(width, width)
		for i in range(width):
			result[i, i] = 1.0
		return result

