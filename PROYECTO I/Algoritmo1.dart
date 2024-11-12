//David Sumba Correa
void main() {
  int edad = 20;
  double altura = 1.70;
  String nombre = "Carlos";
  bool esEstudiante = true;

  num peso = 65.5;
  dynamic flexible = "Texto";
  Object persona = "Juan";

  String apellido = "Pérez";

  List<int> numeros = [1, 2, 3];
  Set<String> frutas = {"manzana", "pera", "uva"};
  Map<String, int> edades = {
    "Carlos": 20,
    "Ana": 22
  };

  edad += 1;
  altura *= 1.1;
  bool esAdulto = edad >= 18;
  apellido ??= "Desconocido";

  if (esAdulto) {
    print("$nombre es un adulto.");
  } else {
    print("$nombre no es un adulto.");
  }

  for (int i = 0; i < numeros.length; i++) {
    print("Número: ${numeros[i]}");
  }

  print("Edad: $edad");
  print("Altura: $altura");
  print("Peso: $peso");
  print("Nombre: $nombre");
  print("Apellido: $apellido");
}
