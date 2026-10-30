using System;
using System.Collections.Generic;

namespace Lab2
{
    public static class RegistrationMenu
    {
        public static void Show()
        {
            while (true)
            {
                ConsoleHelper.Clear();
                Console.WriteLine("====== Registration Management ======");
                Console.WriteLine("1. Register Student to Course");
                Console.WriteLine("2. Unregister Student from Course");
                Console.WriteLine("3. View All Registrations");
                Console.WriteLine("4. Back to Main Menu");
                int choice = ConsoleHelper.ReadMenuChoice(4);
                if (choice == 4)
                    return;

                Console.WriteLine();
                ConsoleHelper.Run(() =>
                {
                    switch (choice)
                    {
                        case 1: RegisterStudent(); break;
                        case 2: UnregisterStudent(); break;
                        case 3: ViewAllRegistrations(); break;
                    }
                });
                ConsoleHelper.Pause();
            }
        }

        private static void RegisterStudent()
        {
            Student student = Student.Find(ConsoleHelper.ReadRequired("Enter Student Registration Number: ", 15));
            if (student == null)
            {
                Console.WriteLine("Student not found.");
                return;
            }

            Course course = Course.Find(ConsoleHelper.ReadRequired("Enter Course ID: ", 10));
            if (course == null)
            {
                Console.WriteLine("Course not found.");
                return;
            }

            var enrollment = new Enrollment(student.RegNo, course.CourseId);
            if (enrollment.IsRegistered())
            {
                Console.WriteLine($"{student.Name} is already registered in {course.CourseName}.");
                return;
            }

            enrollment.Register();
            Console.WriteLine($"{student.Name} ({student.RegNo}) registered in {course.CourseName} ({course.CourseId}).");
        }

        private static void UnregisterStudent()
        {
            string regNo = ConsoleHelper.ReadRequired("Enter Student Registration Number: ", 15);
            string courseId = ConsoleHelper.ReadRequired("Enter Course ID: ", 10);

            var enrollment = new Enrollment(regNo, courseId);
            if (!enrollment.IsRegistered())
            {
                Console.WriteLine($"Student {regNo} is not registered in course {courseId}.");
                return;
            }

            enrollment.Unregister();
            Console.WriteLine($"Student {regNo} unregistered from course {courseId}.");
        }

        private static void ViewAllRegistrations()
        {
            List<Enrollment> enrollments = Enrollment.GetAll();
            if (enrollments.Count == 0)
            {
                Console.WriteLine("No registrations found.");
                return;
            }

            Console.WriteLine($"{"Course ID",-12} {"Course Name",-30} {"Reg No",-15} Student Name");
            Console.WriteLine(new string('-', 85));
            foreach (Enrollment enrollment in enrollments)
                Console.WriteLine($"{enrollment.CourseId,-12} {enrollment.CourseName,-30} {enrollment.StudentRegNo,-15} {enrollment.StudentName}");
            Console.WriteLine($"\nTotal registrations: {enrollments.Count}");
        }
    }
}
