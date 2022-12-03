from django.test import TestCase

from diary.models import (
    Books,
    MyUser,
    SchoolClass,
    StudentRegistration,
    TeacherRegistration,
    School,
)


class AccountCreateTest(TestCase):
    def test_invalid_creation_user(self):
        """Check User model validators."""
        book = Books.objects.create(book_name="some_book")
        school = School.objects.create(name_school="some_name_school")
        student_class = SchoolClass.objects.create(
            number_class=1, name_class="A", slug="a", school=school
        )

        teacher_model = TeacherRegistration.objects.create(item=book)
        student = StudentRegistration.objects.create(learned_class=student_class)

        with self.assertRaises(ValueError):
            MyUser.objects.create_user(
                username="some",
                password="Www122244",
                first_name="some",
                last_name="some",
                teacher=teacher_model,
            )

        with self.assertRaises(ValueError):
            MyUser.objects.create_user(
                username="some",
                password="Www122244",
                first_name="some",
                last_name="some",
                invitation_token="some",
            )

        with self.assertRaises(ValueError):
            MyUser.objects.create_user(
                username="some",
                password="Www122244",
                first_name="some",
                last_name="some",
                invitation_token="some",
                teacher=teacher_model,
                student=student,
            )
