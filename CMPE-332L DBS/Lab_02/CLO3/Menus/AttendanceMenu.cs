using System;
using System.Collections.Generic;
using System.Linq;

namespace Lab2
{
    public static class AttendanceMenu
    {
        public static void Show()
        {
            while (true)
            {
                ConsoleHelper.Clear();
                Console.WriteLine("====== Attendance Management ======");
                Console.WriteLine("1. Mark Attendance");
                Console.WriteLine("2. Edit Attendance");
                Console.WriteLine("3. View Attendance by Date");
                Console.WriteLine("4. Back to Main Menu");
                int choice = ConsoleHelper.ReadMenuChoice(4);
                if (choice == 4)
                    return;

                Console.WriteLine();
                ConsoleHelper.Run(() =>
                {
                    switch (choice)
                    {
                        case 1: MarkAttendance(); break;
                        case 2: EditAttendance(); break;
                        case 3: ViewAttendanceByDate(); break;
                    }
                });
                ConsoleHelper.Pause();
            }
        }

        private static void MarkAttendance()
        {
            Course course = Course.Find(ConsoleHelper.ReadRequired("Enter Course ID: ", 10));
            if (course == null)
            {
                Console.WriteLine("Course not found.");
                return;
            }

            DateTime date = ConsoleHelper.ReadDate("Enter Date");
            string day = date.ToString(ConsoleHelper.DateFormat);

            // Only students without a record for this date are asked, so students registered later can still be marked.
            List<Student> students = Attendance.GetUnmarkedStudents(course.CourseId, date);
            if (students.Count == 0)
            {
                if (Enrollment.CountInCourse(course.CourseId) == 0)
                    Console.WriteLine($"No students are registered in {course.CourseName}.");
                else
                    Console.WriteLine($"Attendance for {course.CourseName} on {day} is already marked. Use Edit Attendance to change it.");
                return;
            }

            Console.WriteLine($"\nMarking attendance for {course.CourseName} ({course.CourseId}) on {day}");
            Console.WriteLine("Enter P for present or A for absent.\n");

            DateTime timeStamp = date.Date + DateTime.Now.TimeOfDay;
            var records = new List<Attendance>();
            foreach (Student student in students)
            {
                bool present = ConsoleHelper.ReadPresentAbsent($"{student.RegNo} - {student.Name}: ");
                records.Add(new Attendance(student.RegNo, course.CourseId, timeStamp, present));
            }

            Attendance.SaveAll(records);
            int presentCount = records.Count(r => r.Status);
            Console.WriteLine($"\nAttendance saved for {records.Count} student(s): {presentCount} present, {records.Count - presentCount} absent.");
        }

        private static void EditAttendance()
        {
            Course course = Course.Find(ConsoleHelper.ReadRequired("Enter Course ID: ", 10));
            if (course == null)
            {
                Console.WriteLine("Course not found.");
                return;
            }

            DateTime date = ConsoleHelper.ReadDate("Enter Date");
            List<Attendance> records = Attendance.GetByDate(date, course.CourseId);
            if (records.Count == 0)
            {
                Console.WriteLine($"No attendance is marked for {course.CourseName} on {date.ToString(ConsoleHelper.DateFormat)}.");
                return;
            }

            Console.WriteLine();
            PrintAttendance(records);
            Console.WriteLine();

            string regNo = ConsoleHelper.ReadRequired("Enter Registration Number of the student to edit: ", 15);
            bool present = ConsoleHelper.ReadPresentAbsent("New status (P/A): ");

            if (Attendance.UpdateStatus(regNo, course.CourseId, date, present) == 0)
                Console.WriteLine($"Student {regNo} has no attendance record for this course on that date.");
            else
                Console.WriteLine($"Attendance of {regNo} changed to {ConsoleHelper.StatusText(present)}.");
        }

        private static void ViewAttendanceByDate()
        {
            DateTime date = ConsoleHelper.ReadDate("Enter Date");
            string courseId = ConsoleHelper.ReadOptional("Enter Course ID (Enter for all courses): ", 10);

            if (courseId != null && Course.Find(courseId) == null)
            {
                Console.WriteLine("Course not found.");
                return;
            }

            List<Attendance> records = Attendance.GetByDate(date, courseId);
            string day = date.ToString(ConsoleHelper.DateFormat);
            if (records.Count == 0)
            {
                Console.WriteLine($"No attendance found for {day}.");
                return;
            }

            Console.WriteLine($"\nAttendance on {day}\n");
            PrintAttendance(records);
        }

        private static void PrintAttendance(List<Attendance> records)
        {
            Console.WriteLine($"{"Course ID",-12} {"Reg No",-15} {"Name",-25} {"Time",-9} Status");
            Console.WriteLine(new string('-', 72));
            foreach (Attendance record in records)
                Console.WriteLine($"{record.CourseId,-12} {record.StudentRegNo,-15} {record.StudentName,-25} {record.TimeStamp,-9:HH:mm} {ConsoleHelper.StatusText(record.Status)}");

            int presentCount = records.Count(r => r.Status);
            Console.WriteLine($"\nPresent: {presentCount}   Absent: {records.Count - presentCount}   Total: {records.Count}");
        }
    }
}
