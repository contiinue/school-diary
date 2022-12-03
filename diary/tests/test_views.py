from django.test import TestCase
from django.urls import reverse

from diary.models import (
    Books,
    MyUser,
    SchoolClass,
    StudentRegistration,
    TeacherRegistration,
    TokenRegistration,
    School,
)


class RegistrationTests(TestCase):
    def test_create_student(self):
        """testing registration form for student."""
        school = School.objects.create(name_school="some_name_school")
        student_class = SchoolClass.objects.create(
            number_class=1, name_class="A", slug="a", school=school
        )
        token = TokenRegistration.objects.create(
            who_registration="student", student_class=student_class, school=school
        )
        url = f'{reverse("register")}?request_form=student'

        response = self.client.post(
            url,
            data={
                "username": "some",
                "password1": "Www122244",
                "password2": "Www122244",
                "first_name": "Alex",
                "email": "soeem@dfssdf.sdf",
                "last_name": "Smith",
                "learned_class": "1",
                "age": "15",
                "invitation_token": token.token,
            },
        )

        self.assertEqual(302, response.status_code)
        self.assertEqual(1, MyUser.objects.all().count())
        self.assertIsNotNone(self.client.cookies.get("sessionid"))

    def test_create_teacher(self):
        """testing registration form for teacher."""
        school = School.objects.create(name_school="some_name_school")
        book = Books.objects.create(book_name="some_name_book")
        token = TokenRegistration.objects.create(
            who_registration="teacher", school=school
        )
        url = f'{reverse("register")}?request_form=teacher'
        response = self.client.post(
            url,
            data={
                "username": "some",
                "password1": "Www122244",
                "password2": "Www122244",
                "first_name": "Alex",
                "email": "soeem@dfssdf.sdf",
                "last_name": "Smith",
                "item": book.pk,
                "age": "15",
                "invitation_token": token.token,
            },
        )

        self.assertEqual(302, response.status_code)
        self.assertEqual(1, MyUser.objects.all().count())
        self.assertIsNotNone(self.client.cookies.get("sessionid"))


class PermissionsTest(TestCase):
    def setUp(self) -> None:
        """Create Student and Teacher model and more models for registration."""
        book = Books.objects.create(book_name="some_book")
        school = School.objects.create(name_school="some_name_school")
        student_class = SchoolClass.objects.create(
            number_class=1, name_class="A", slug="a", school=school
        )
        self.teacher_token = TokenRegistration.objects.create(
            who_registration="teacher", school=school
        )
        self.student_token = TokenRegistration.objects.create(
            who_registration="student", student_class=student_class, school=school
        )

        self.teacher_model = TeacherRegistration.objects.create(item=book)
        self.student = StudentRegistration.objects.create(learned_class=student_class)

        MyUser.objects.create_user(
            username="teacher",
            password="Www122244",
            email="teacher@some.re",
            first_name="some",
            last_name="some",
            teacher=self.teacher_model,
            invitation_token=self.teacher_token,
        )

        MyUser.objects.create_user(
            username="student",
            password="Www122244",
            email="student@some.re",
            first_name="some",
            last_name="some",
            student=self.student,
            invitation_token=self.student_token,
        )

    def test_permissions_for_teacher(self):
        """Check permissions for teacher."""

        self.client.login(username="teacher", password="Www122244")

        self.assertEqual(
            403,
            self.client.get(
                reverse("student", kwargs={"username": "student"})
            ).status_code,
        )
        self.assertEqual(
            403,
            self.client.get(
                reverse("homework", kwargs={"username": "student"})
            ).status_code,
        )

    def test_permissions_for_student(self):
        """Check permissions for student."""
        self.client.login(username="student", password="Www122244")
        self.assertEqual(
            403,
            self.client.get(
                reverse("student-class", kwargs={"class_number": "1", "slug_name": "a"})
            ).status_code,
        )
        self.assertEqual(403, self.client.get(reverse("teacher")).status_code)
