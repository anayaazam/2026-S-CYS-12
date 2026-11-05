package Courses;
class Student {
    String name;
    Course[] courses = new Course[10];
    int courseCount = 0;
    Student(String name) {
        this.name = name;
    }
    boolean isEnrolledIn(Course course) {
        for (int i = 0; i < courseCount; i++) {
            if (courses[i] == course) {
                return true;
            }
        }
        return false;
    }
    void enroll(Course course) {
        if (isEnrolledIn(course)) {
            System.out.println(name + " is already enrolled in " + course.name);
        } else if (courseCount == courses.length) {
            System.out.println(name + " cannot take more courses");
        } else if (course.isFull()) {
            System.out.println(course.name + " is full");
        } else {
            courses[courseCount] = course;
            courseCount++;
            course.addStudent(this);
            System.out.println(name + " enrolled in " + course.name);
        }
    }
    void showCourses() {
        System.out.print(name + " takes: ");
        for (int i = 0; i < courseCount; i++) {
            System.out.print(courses[i].name + " ");
        }
        System.out.println();
    }
    @Override
    public String toString() {
        return name;
    }
}
