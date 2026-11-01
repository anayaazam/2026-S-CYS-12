using System;
namespace LO1
{
    class P1Task4
    {
        public static void Main()
        {
            int number;
            Console.Write("Enter a number: ");
            while (!int.TryParse(Console.ReadLine(), out number))
            {
                Console.Write("Please enter a whole number: ");
            }

            if (number % 2 == 0)
            {
                Console.WriteLine($"{number} is even.");
            }
            else
            {
                Console.WriteLine($"{number} is odd.");
            }
        }
    }
}
