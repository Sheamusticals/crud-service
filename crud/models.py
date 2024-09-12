from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=255)
    head = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Lecturer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    department = models.ForeignKey(Department, related_name='lecturers', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    department = models.ForeignKey(Department, related_name='courses', on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, related_name='courses', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    department = models.ForeignKey(Department, related_name='students', on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, through='Enrollment', related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Classroom(models.Model):
    room_number = models.CharField(max_length=10)
    building = models.CharField(max_length=255)

    def __str__(self):
        return f"Room {self.room_number}, {self.building}"

class Schedule(models.Model):
    course = models.ForeignKey(Course, related_name='schedules', on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, related_name='schedules', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.course} in {self.classroom} on {self.day_of_week}"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"
