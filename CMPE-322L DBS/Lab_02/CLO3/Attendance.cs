using System;
using System.Collections.Generic;
using System.Linq;
using MySql.Data.MySqlClient;

namespace Lab2
{
    public class Attendance
    {
        public string StudentRegNo { get; set; }
        public string StudentName { get; set; }
        public string CourseId { get; set; }
        public DateTime TimeStamp { get; set; }
        public bool Status { get; set; }   // true = present, false = absent

        public Attendance(string studentRegNo, string courseId, DateTime timeStamp, bool status, string studentName = null)
        {
            StudentRegNo = studentRegNo;
            CourseId = courseId;
            TimeStamp = timeStamp;
            Status = status;
            StudentName = studentName;
        }

        // Saves a whole class list at once so a half-marked list is never stored.
        public static void SaveAll(List<Attendance> records)
        {
            string query = "INSERT INTO Attendance (StudentRegNo, Course_ID, TimeStamp, Status) " +
                           "VALUES (@regNo, @courseId, @timeStamp, @status)";

            var statements = records.Select(record => (query, new[]
            {
                new MySqlParameter("@regNo", record.StudentRegNo),
                new MySqlParameter("@courseId", record.CourseId),
                new MySqlParameter("@timeStamp", record.TimeStamp),
                new MySqlParameter("@status", record.Status)
            })).ToArray();

            DatabaseHelper.Instance.UpdateInTransaction(statements);
        }

        // Returns the number of records found for the student on that date (0 means nothing was marked).
        public static int UpdateStatus(string regNo, string courseId, DateTime date, bool status)
        {
            string query = "UPDATE Attendance SET Status = @status " +
                           "WHERE StudentRegNo = @regNo AND Course_ID = @courseId " +
                           "AND TimeStamp >= @dayStart AND TimeStamp < @dayEnd";

            return DatabaseHelper.Instance.Update(query,
                new MySqlParameter("@status", status),
                new MySqlParameter("@regNo", regNo),
                new MySqlParameter("@courseId", courseId),
                new MySqlParameter("@dayStart", date.Date),
                new MySqlParameter("@dayEnd", date.Date.AddDays(1)));
        }

        // courseId == null lists every course.
        public static List<Attendance> GetByDate(DateTime date, string courseId)
        {
            string query = "SELECT a.StudentRegNo, s.Name, a.Course_ID, a.TimeStamp, a.Status " +
                           "FROM Attendance a " +
                           "JOIN Student s ON s.RegistrationNumber = a.StudentRegNo " +
                           "WHERE a.TimeStamp >= @dayStart AND a.TimeStamp < @dayEnd " +
                           "AND (@courseId IS NULL OR a.Course_ID = @courseId) " +
                           "ORDER BY a.Course_ID, a.StudentRegNo";

            var records = new List<Attendance>();
            using (var reader = DatabaseHelper.Instance.GetData(query,
                new MySqlParameter("@dayStart", date.Date),
                new MySqlParameter("@dayEnd", date.Date.AddDays(1)),
                new MySqlParameter("@courseId", (object)courseId ?? DBNull.Value)))
            {
                while (reader.Read())
                {
                    records.Add(new Attendance(
                        reader["StudentRegNo"].ToString(),
                        reader["Course_ID"].ToString(),
                        Convert.ToDateTime(reader["TimeStamp"]),
                        Convert.ToBoolean(reader["Status"]),
                        reader["Name"].ToString()));
                }
            }
            return records;
        }

        // Registered students of the course who have no attendance record on that date yet.
        public static List<Student> GetUnmarkedStudents(string courseId, DateTime date)
        {
            string query = "SELECT DISTINCT s.RegistrationNumber, s.Name " +
                           "FROM Enrollments e " +
                           "JOIN Student s ON s.RegistrationNumber = e.StudentRegNo " +
                           "WHERE e.Course_ID = @courseId " +
                           "AND NOT EXISTS (SELECT 1 FROM Attendance a " +
                           "                WHERE a.StudentRegNo = e.StudentRegNo AND a.Course_ID = e.Course_ID " +
                           "                AND a.TimeStamp >= @dayStart AND a.TimeStamp < @dayEnd) " +
                           "ORDER BY s.RegistrationNumber";

            var students = new List<Student>();
            using (var reader = DatabaseHelper.Instance.GetData(query,
                new MySqlParameter("@courseId", courseId),
                new MySqlParameter("@dayStart", date.Date),
                new MySqlParameter("@dayEnd", date.Date.AddDays(1))))
            {
                while (reader.Read())
                    students.Add(new Student(reader["RegistrationNumber"].ToString(), reader["Name"].ToString()));
            }
            return students;
        }
    }
}
