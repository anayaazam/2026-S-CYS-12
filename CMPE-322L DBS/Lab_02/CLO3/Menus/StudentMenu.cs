using System;
using System.Collections.Generic;

namespace Lab2
{
    public static class StudentMenu
    {
        public static void Show()
        {
            while (true)
            {
                ConsoleHelper.Clear();
                Console.WriteLine("====== Student Management ======");
                Console.WriteLine("1. Add Student");
                Console.WriteLine("2. Edit Student");
                Console.WriteLine("3. Delete Student");
                Console.WriteLine("4. Search Student");
                Console.WriteLine("5. View All Students");
                Console.WriteLine("6. Back to Main Menu");
                int choice = ConsoleHelper.ReadMenuChoice(6);
                if (choice == 6)
                    return;

                Console.WriteLine();
                ConsoleHelper.Run(() =>
                {
                    switch (choice)
                    {
                        case 1: AddStudent(); break;
                        case 2: EditStudent(); break;
                        case 3: DeleteStudent(); break;
                        case 4: SearchStudent(); break;
                        case 5: ViewAllStudents(); break;
                    }
                });
                ConsoleHelper.Pause();
            }
        }

        private static void AddStudent()
        {
            string regNo = ConsoleHelper.ReadRequired("Enter Registration Number: ", 15);
            if (Student.Find(regNo) != null)
            {
                Console.WriteLine($"A student with registration number {regNo} already exists.");
                return;
            }

            string name = ConsoleHelper.ReadRequired("Enter Name: ", 100);
            string department = ConsoleHelper.ReadRequired("Enter Department: ", 50);
            int session = ConsoleHelper.ReadInt("Enter Session (e.g. 2024): ", 1900, 2100);
            string address = ConsoleHelper.ReadOptional("Enter Address (optional): ", 255);

            var student = new Student(regNo, name, department, session, address);
            student.AddStudent();
            Console.WriteLine("Student added successfully.");
        }

        private static void EditStudent()
        {
            string regNo = ConsoleHelper.ReadRequired("Enter Registration Number of the student to edit: ", 15);
            Student student = Student.Find(regNo);
            if (student == null)
            {
                Console.WriteLine("Student not found.");
                return;
            }

            Console.WriteLine("Press Enter to keep the current value.");
            student.Name = ConsoleHelper.ReadWithDefault("Name", student.Name, 100);
            student.Department = ConsoleHelper.ReadWithDefault("Department", student.Department, 50);
            student.Session = ConsoleHelper.ReadIntWithDefault("Session", student.Session, 1900, 2100);
            student.Address = ConsoleHelper.ReadWithDefault("Address", student.Address, 255);

            student.EditStudent();
            Console.WriteLine("Student updated successfully.");
        }

        private static void DeleteStudent()
        {
            string regNo = ConsoleHelper.ReadRequired("Enter Registration Number of the student to delete: ", 15);
            Student student = Student.Find(regNo);
            if (student == null)
            {
                Console.WriteLine("Student not found.");
                return;
            }

            Console.WriteLine("The student's course registrations and attendance records will also be deleted.");
            if (!ConsoleHelper.ReadYesNo($"Delete {student.Name} ({student.RegNo})? (y/n): "))
            {
                Console.WriteLine("Delete cancelled.");
                return;
            }

            student.DeleteStudent();
            Console.WriteLine("Student deleted successfully.");
        }

        private static void SearchStudent()
        {
            string regNo = ConsoleHelper.ReadRequired("Enter Registration Number: ", 15);
            Student student = Student.Find(regNo);
            if (student == null)
            {
                Console.WriteLine("Student not found.");
                return;
            }

            Console.WriteLine();
            Console.WriteLine($"Registration No : {student.RegNo}");
            Console.WriteLine($"Name            : {student.Name}");
            Console.WriteLine($"Department      : {student.Department}");
            Console.WriteLine($"Session         : {student.Session}");
            Console.WriteLine($"Address         : {student.Address}");
        }

        private static void ViewAllStudents()
        {
            List<Student> students = Student.GetAll();
            if (students.Count == 0)
            {
                Console.WriteLine("No students found.");
                return;
            }

            Console.WriteLine($"{"Reg No",-15} {"Name",-25} {"Department",-25} {"Session",-8} Address");
            Console.WriteLine(new string('-', 90));
            foreach (Student student in students)
                Console.WriteLine($"{student.RegNo,-15} {student.Name,-25} {student.Department,-25} {student.Session,-8} {student.Address}");
            Console.WriteLine($"\nTotal students: {students.Count}");
        }
    }
}
