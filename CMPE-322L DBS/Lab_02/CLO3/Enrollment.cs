using System;
using System.Collections.Generic;
using MySql.Data.MySqlClient;

namespace Lab2
{
    public class Enrollment
    {
        public string StudentRegNo { get; set; }
        public string CourseId { get; set; }

        // Filled only when enrollments are read together with the Student and Course tables.
        public string StudentName { get; private set; }
        public string CourseName { get; private set; }

        public Enrollment(string studentRegNo, string courseId)
        {
            StudentRegNo = studentRegNo;
            CourseId = courseId;
        }

        public void Register()
        {
            string query = "INSERT INTO Enrollments (StudentRegNo, Course_ID) VALUES (@regNo, @courseId)";
            DatabaseHelper.Instance.Update(query, AllParameters());
        }

        public void Unregister()
        {
            string query = "DELETE FROM Enrollments WHERE StudentRegNo = @regNo AND Course_ID = @courseId";
            DatabaseHelper.Instance.Update(query, AllParameters());
        }

        // The Enrollments table has no primary key, so duplicates are prevented here instead.
        public bool IsRegistered()
        {
            string query = "SELECT COUNT(*) FROM Enrollments WHERE StudentRegNo = @regNo AND Course_ID = @courseId";
            return Convert.ToInt32(DatabaseHelper.Instance.GetScalar(query, AllParameters())) > 0;
        }

        public static int CountInCourse(string courseId)
        {
            string query = "SELECT COUNT(DISTINCT StudentRegNo) FROM Enrollments WHERE Course_ID = @courseId";
            return Convert.ToInt32(DatabaseHelper.Instance.GetScalar(query, new MySqlParameter("@courseId", courseId)));
        }

        public static List<Enrollment> GetAll()
        {
            string query = "SELECT DISTINCT e.StudentRegNo, s.Name, e.Course_ID, c.Course_Name " +
                           "FROM Enrollments e " +
                           "JOIN Student s ON s.RegistrationNumber = e.StudentRegNo " +
                           "JOIN Course c ON c.Course_ID = e.Course_ID " +
                           "ORDER BY e.Course_ID, e.StudentRegNo";

            var enrollments = new List<Enrollment>();
            using (var reader = DatabaseHelper.Instance.GetData(query))
            {
                while (reader.Read())
                {
                    enrollments.Add(new Enrollment(reader["StudentRegNo"].ToString(), reader["Course_ID"].ToString())
                    {
                        StudentName = reader["Name"].ToString(),
                        CourseName = reader["Course_Name"].ToString()
                    });
                }
            }
            return enrollments;
        }

        private MySqlParameter[] AllParameters()
        {
            return new[]
            {
                new MySqlParameter("@regNo", StudentRegNo),
                new MySqlParameter("@courseId", CourseId)
            };
        }
    }
}
