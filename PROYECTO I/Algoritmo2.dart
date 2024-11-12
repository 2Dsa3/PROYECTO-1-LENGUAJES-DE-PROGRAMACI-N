void main() {
  int a = 10;
  int b = 3;
  int result;

  result = a - b;
  
  result = a * b; 
  
  result = a ~/ b;

  result = a % b; 
  
  a++; 
  a--;

  bool isEqual = (a == b); 
  bool isNotEqual = (a != b); 
  bool greaterThan = (a > b); 
  bool lessThan = (a < b); 
  bool greaterOrEqual = (a >= b); 
  bool lessOrEqual = (a <= b); 
  String text = 'Dart';
  bool andOperator = (a > b && b > 0); 
  bool orOperator = (a > b || b < 0); 

    if (result > 0) {
        result++;
    } else {
        result--;
    }

   while (result < 3) {
    result++;
  }


}
