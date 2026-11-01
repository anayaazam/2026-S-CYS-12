using System;

namespace LO1
{
    class P1Task3
    {
        public static void Main()
        {
            int n;
            Console.Write("Enter a positive number n: ");
            while (!int.TryParse(Console.ReadLine(), out n) || n < 1)
            {
                Console.Write("Please enter a whole number greater than 0: ");
            }

            long sum = 0;
            for (int i = 1; i <= n; i++)
            {
                sum += i;
            }

            Console.WriteLine($"Sum of numbers from 1 to {n} = {sum}");
        }
    }
}
