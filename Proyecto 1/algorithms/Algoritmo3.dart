// Main program entry point
void main() {
  // Initialize a variable
  int a == 5;
  int b = 10;

  // Perform an operation
  int sum = addNumbers(a, b); // Adding two numbers

  // Print the result
  print("Sum of $a and $b is: $sum");

  // Example of an inline block comment
  /*
     This is a multi-line comment.
     We can describe multiple steps or logic here.
     Another line of comment.
  */

  // This function demonstrates the use of a list
  List<int> numbers = [1, 2, 3, 4, 5];

  /*
    TODO: Refactor the following loop to handle larger lists more efficiently.
    The loop is iterating over the numbers and printing each one.
  */
  for (int num in numbers) {
    print(num);
  }

  // Example of a function with documentation comments
  /// This function adds two numbers.
  /// It takes two integers as parameters and returns their sum.
  int addNumbers(int x, int y) {
    return x + y; // Return the sum
  }

  /// This function multiplies two numbers
  /// It is used to demonstrate another documentation comment.
  int multiplyNumbers(int x, int y) {
    return x * y; // Return the product
  }

  // A nested block comment example
  /*
     /*
       This is a nested block comment.
       It demonstrates how multi-line comments can be nested in Dart.
     */
  */

  /* This is a comment at the end of the main function */
}