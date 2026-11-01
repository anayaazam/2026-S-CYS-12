using System;
using System.Collections.Generic;

namespace Lab2
{
    public static class CourseMenu
    {
        public static void Show()
        {
            while (true)
            {
                ConsoleHelper.Clear();
                Console.WriteLine("====== Course Management ======");
                Console.WriteLine("1. Add Course");
                Console.WriteLine("2. Edit Course");
                Console.WriteLine("3. Delete Course");
                Console.WriteLine("4. View All Courses");
                Console.WriteLine("5. Back to Main Menu");
                int choice = ConsoleHelper.ReadMenuChoice(5);
                if (choice == 5)
                    return;

                Console.WriteLine();
                ConsoleHelper.Run(() =>
                {
                    switch (choice)
                    {
                        case 1: AddCourse(); break;
                        case 2: EditCourse(); break;
                        case 3: DeleteCourse(); break;
                        case 4: ViewAllCourses(); break;
                    }
                });
                ConsoleHelper.Pause();
            }
        }

        private static void AddCourse()
        {
            string courseId = ConsoleHelper.ReadRequired("Enter Course ID: ", 10);
            if (Course.Find(courseId) != null)
            {
                Console.WriteLine($"A course with ID {courseId} already exists.");
                return;
            }

            string courseName = ConsoleHelper.ReadRequired("Enter Course Name: ", 100);

            var course = new Course(courseId, courseName);
            course.AddCourse();
            Console.WriteLine("Course added successfully.");
        }

        private static void EditCourse()
        {
            string courseId = ConsoleHelper.ReadRequired("Enter Course ID of the course to edit: ", 10);
            Course course = Course.Find(courseId);
            if (course == null)
            {
                Console.WriteLine("Course not found.");
                return;
            }

            Console.WriteLine("Press Enter to keep the current value.");
            course.CourseName = ConsoleHelper.ReadWithDefault("Course Name", course.CourseName, 100);

            course.EditCourse();
            Console.WriteLine("Course updated successfully.");
        }

        private static void DeleteCourse()
        {
            string courseId = ConsoleHelper.ReadRequired("Enter Course ID of the course to delete: ", 10);
            Course course = Course.Find(courseId);
            if (course == null)
            {
                Console.WriteLine("Course not found.");
                return;
            }

            Console.WriteLine("All registrations and attendance records of this course will also be deleted.");
            if (!ConsoleHelper.ReadYesNo($"Delete {course.CourseName} ({course.CourseId})? (y/n): "))
            {
                Console.WriteLine("Delete cancelled.");
                return;
            }

            course.DeleteCourse();
            Console.WriteLine("Course deleted successfully.");
        }

        private static void ViewAllCourses()
        {
            List<Course> courses = Course.GetAll();
            if (courses.Count == 0)
            {
                Console.WriteLine("No courses found.");
                return;
            }

            Console.WriteLine($"{"Course ID",-12} Course Name");
            Console.WriteLine(new string('-', 50));
            foreach (Course course in courses)
                Console.WriteLine($"{course.CourseId,-12} {course.CourseName}");
            Console.WriteLine($"\nTotal courses: {courses.Count}");
        }
    }
}
