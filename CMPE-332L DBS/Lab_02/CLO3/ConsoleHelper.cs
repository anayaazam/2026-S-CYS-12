using System;
using System.Globalization;
using MySql.Data.MySqlClient;

namespace Lab2
{
    // Input and screen helpers shared by all menus. Every Read* method keeps asking until the input is valid.
    public static class ConsoleHelper
    {
        public const string DateFormat = "yyyy-MM-dd";

        public static string ReadLine()
        {
            string line = Console.ReadLine();
            if (line == null)   // input stream closed (Ctrl+Z / end of piped input): nothing more to read
                Environment.Exit(0);
            return line.Trim();
        }

        public static int ReadMenuChoice(int optionCount)
        {
            return ReadInt($"Select an option (1-{optionCount}): ", 1, optionCount);
        }

        public static string ReadRequired(string prompt, int maxLength)
        {
            while (true)
            {
                Console.Write(prompt);
                string value = ReadLine();
                if (value.Length == 0)
                    Console.WriteLine("This field is required.");
                else if (value.Length > maxLength)
                    Console.WriteLine($"Please enter at most {maxLength} characters.");
                else
                    return value;
            }
        }

        // Returns null when the user leaves the field blank.
        public static string ReadOptional(string prompt, int maxLength)
        {
            while (true)
            {
                Console.Write(prompt);
                string value = ReadLine();
                if (value.Length > maxLength)
                    Console.WriteLine($"Please enter at most {maxLength} characters.");
                else
                    return value.Length == 0 ? null : value;
            }
        }

        // Shows the current value in brackets; pressing Enter keeps it.
        public static string ReadWithDefault(string label, string current, int maxLength)
        {
            while (true)
            {
                Console.Write($"{label} [{current}]: ");
                string value = ReadLine();
                if (value.Length == 0)
                    return current;
                if (value.Length > maxLength)
                    Console.WriteLine($"Please enter at most {maxLength} characters.");
                else
                    return value;
            }
        }

        public static int ReadInt(string prompt, int min, int max)
        {
            while (true)
            {
                Console.Write(prompt);
                if (int.TryParse(ReadLine(), out int value) && value >= min && value <= max)
                    return value;
                Console.WriteLine($"Please enter a whole number from {min} to {max}.");
            }
        }

        public static int ReadIntWithDefault(string label, int current, int min, int max)
        {
            while (true)
            {
                Console.Write($"{label} [{current}]: ");
                string input = ReadLine();
                if (input.Length == 0)
                    return current;
                if (int.TryParse(input, out int value) && value >= min && value <= max)
                    return value;
                Console.WriteLine($"Please enter a whole number from {min} to {max}.");
            }
        }

        // Pressing Enter picks today's date.
        public static DateTime ReadDate(string prompt)
        {
            while (true)
            {
                Console.Write($"{prompt} ({DateFormat}, Enter for today): ");
                string input = ReadLine();
                if (input.Length == 0)
                    return DateTime.Today;
                if (DateTime.TryParseExact(input, DateFormat, CultureInfo.InvariantCulture, DateTimeStyles.None, out DateTime date))
                    return date;
                Console.WriteLine($"Please enter the date as {DateFormat}, for example {DateTime.Today.ToString(DateFormat)}.");
            }
        }

        public static bool ReadYesNo(string prompt)
        {
            while (true)
            {
                Console.Write(prompt);
                string input = ReadLine().ToUpperInvariant();
                if (input == "Y" || input == "YES") return true;
                if (input == "N" || input == "NO") return false;
                Console.WriteLine("Please enter y or n.");
            }
        }

        // true = present, false = absent
        public static bool ReadPresentAbsent(string prompt)
        {
            while (true)
            {
                Console.Write(prompt);
                string input = ReadLine().ToUpperInvariant();
                if (input == "P") return true;
                if (input == "A") return false;
                Console.WriteLine("Please enter P for present or A for absent.");
            }
        }

        public static string StatusText(bool present)
        {
            return present ? "Present" : "Absent";
        }

        // Runs one menu action and reports database errors instead of crashing the program.
        public static void Run(Action action)
        {
            try
            {
                action();
            }
            catch (MySqlException ex)
            {
                Console.WriteLine("Database error: " + ex.Message);
            }
        }

        public static void Pause()
        {
            Console.WriteLine();
            Console.Write("Press Enter to continue...");
            ReadLine();
        }

        public static void Clear()
        {
            if (!Console.IsOutputRedirected)
                Console.Clear();
        }
    }
}
