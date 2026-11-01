using System;
namespace LO1
    class P1Task5
    {
        public static void Main()
        {
            Console.Write("Enter a string: ");
            string text = Console.ReadLine();

            foreach (char c in text)
            {
                Console.WriteLine(c);
            }
        }
    }
}
