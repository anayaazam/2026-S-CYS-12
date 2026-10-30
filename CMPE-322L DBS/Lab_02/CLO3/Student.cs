using System;
using System.Collections.Generic;
using MySql.Data.MySqlClient;

namespace Lab2
{
    public class Student
    {
        public string RegNo { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
        public int Session { get; set; }
        public string Address { get; set; }

        public Student(string regNo, string name = null, string department = null, int session = 0, string address = null)
        {
            RegNo = regNo;
            Name = name;
            Department = department;
            Session = session;
            Address = address;
        }

        public void AddStudent()
        {
            string query = "INSERT INTO Student (RegistrationNumber, Name, Department, Session, Address) " +
                           "VALUES (@regNo, @name, @department, @session, @address)";
            DatabaseHelper.Instance.Update(query, AllParameters());
        }

        public void EditStudent()
        {
            string query = "UPDATE Student SET Name = @name, Department = @department, Session = @session, Address = @address " +
                           "WHERE RegistrationNumber = @regNo";
            DatabaseHelper.Instance.Update(query, AllParameters());
        }

        // Enrollments and Attendance reference the student, so their rows are removed first.
        public void DeleteStudent()
        {
            DatabaseHelper.Instance.UpdateInTransaction(
                ("DELETE FROM Attendance WHERE StudentRegNo = @regNo", KeyParameter()),
                ("DELETE FROM Enrollments WHERE StudentRegNo = @regNo", KeyParameter()),
                ("DELETE FROM Student WHERE RegistrationNumber = @regNo", KeyParameter()));
        }

        public static Student Find(string regNo)
        {
            string query = "SELECT * FROM Student WHERE RegistrationNumber = @regNo";
            using (var reader = DatabaseHelper.Instance.GetData(query, new MySqlParameter("@regNo", regNo)))
            {
                return reader.Read() ? FromReader(reader) : null;
            }
        }

        public static List<Student> GetAll()
        {
            var students = new List<Student>();
            using (var reader = DatabaseHelper.Instance.GetData("SELECT * FROM Student ORDER BY RegistrationNumber"))
            {
                while (reader.Read())
                    students.Add(FromReader(reader));
            }
            return students;
        }

        private static Student FromReader(MySqlDataReader reader)
        {
            return new Student(
                reader["RegistrationNumber"].ToString(),
                reader["Name"].ToString(),
                reader["Department"].ToString(),
                Convert.ToInt32(reader["Session"]),
                reader["Address"] == DBNull.Value ? null : reader["Address"].ToString());
        }

        private MySqlParameter[] KeyParameter()
        {
            return new[] { new MySqlParameter("@regNo", RegNo) };
        }

        private MySqlParameter[] AllParameters()
        {
            return new[]
            {
                new MySqlParameter("@regNo", RegNo),
                new MySqlParameter("@name", Name),
                new MySqlParameter("@department", Department),
                new MySqlParameter("@session", Session),
                new MySqlParameter("@address", (object)Address ?? DBNull.Value)
            };
        }
    }
}
