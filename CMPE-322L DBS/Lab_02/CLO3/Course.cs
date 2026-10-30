using System.Collections.Generic;
using MySql.Data.MySqlClient;

namespace Lab2
{
    public class Course
    {
        public string CourseId { get; set; }
        public string CourseName { get; set; }

        public Course(string courseId, string courseName = null)
        {
            CourseId = courseId;
            CourseName = courseName;
        }

        public void AddCourse()
        {
            string query = "INSERT INTO Course (Course_ID, Course_Name) VALUES (@courseId, @courseName)";
            DatabaseHelper.Instance.Update(query, AllParameters());
        }

        public void EditCourse()
        {
            string query = "UPDATE Course SET Course_Name = @courseName WHERE Course_ID = @courseId";
            DatabaseHelper.Instance.Update(query, AllParameters());
        }

        // Enrollments and Attendance reference the course, so their rows are removed first.
        public void DeleteCourse()
        {
            DatabaseHelper.Instance.UpdateInTransaction(
                ("DELETE FROM Attendance WHERE Course_ID = @courseId", KeyParameter()),
                ("DELETE FROM Enrollments WHERE Course_ID = @courseId", KeyParameter()),
                ("DELETE FROM Course WHERE Course_ID = @courseId", KeyParameter()));
        }

        public static Course Find(string courseId)
        {
            string query = "SELECT * FROM Course WHERE Course_ID = @courseId";
            using (var reader = DatabaseHelper.Instance.GetData(query, new MySqlParameter("@courseId", courseId)))
            {
                return reader.Read() ? FromReader(reader) : null;
            }
        }

        public static List<Course> GetAll()
        {
            var courses = new List<Course>();
            using (var reader = DatabaseHelper.Instance.GetData("SELECT * FROM Course ORDER BY Course_ID"))
            {
                while (reader.Read())
                    courses.Add(FromReader(reader));
            }
            return courses;
        }

        private static Course FromReader(MySqlDataReader reader)
        {
            return new Course(reader["Course_ID"].ToString(), reader["Course_Name"].ToString());
        }

        private MySqlParameter[] KeyParameter()
        {
            return new[] { new MySqlParameter("@courseId", CourseId) };
        }

        private MySqlParameter[] AllParameters()
        {
            return new[]
            {
                new MySqlParameter("@courseId", CourseId),
                new MySqlParameter("@courseName", CourseName)
            };
        }
    }
}
