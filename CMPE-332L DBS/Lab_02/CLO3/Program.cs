using System;
using MySql.Data.MySqlClient;

namespace Lab2
{
    public class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Welcome to Student Management System");
            if (!CanConnect())
                return;

            while (true)
            {
                ConsoleHelper.Clear();
                Console.WriteLine("====== Main Menu ======");
                Console.WriteLine("1. Student Management");
                Console.WriteLine("2. Course Management");
                Console.WriteLine("3. Registration Management");
                Console.WriteLine("4. Attendance Management");
                Console.WriteLine("5. Exit");

                switch (ConsoleHelper.ReadMenuChoice(5))
                {
                    case 1: StudentMenu.Show(); break;
                    case 2: CourseMenu.Show(); break;
                    case 3: RegistrationMenu.Show(); break;
                    case 4: AttendanceMenu.Show(); break;
                    case 5:
                        Console.WriteLine("Goodbye!");
                        return;
                }
            }
        }

        private static bool CanConnect()
        {
            try
            {
                using (DatabaseHelper.Instance.GetConnection()) { }
                return true;
            }
            catch (MySqlException ex)
            {
                Console.WriteLine();
                Console.WriteLine($"Could not connect to MySQL database '{DatabaseHelper.Instance.DatabaseName}' as user '{DatabaseHelper.Instance.DatabaseUser}'.");
                Console.WriteLine("Reason: " + ex.Message);
                Console.WriteLine();
                Console.WriteLine("Check that:");
                Console.WriteLine("  - the MySQL80 service is running on 127.0.0.1:3306");
                Console.WriteLine("  - Database\\CreateUser.sql has been run as root (creates the user and database)");
                Console.WriteLine("  - Database\\Dbscript.sql has been run (creates the tables)");
                ConsoleHelper.Pause();
                return false;
            }
        }
    }
}
