from django.test import TestCase, Client
from django.urls import reverse
from .models import *
import random, string

# Create your tests here.

class AppTest(TestCase):
    def setUp(self):
        self.client = Client()


    def generate_random_str(self, n: int) -> str:
        return "".join(random.choices(string.ascii_lowercase, k=n))

    def test_home(self):
        res = self.client.get(reverse('home'))
        self.assertEqual(res.status_code, 302)

    def test_login(self):
        res = self.client.get(reverse('login'))
        self.assertEqual(res.status_code, 200)

    def test_student(self):
        res = self.client.get(reverse('student'))
        self.assertEqual(res.status_code, 302)

    def test_student_home(self):
        res = self.client.get(reverse('student_home', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_student_profile(self):
        res = self.client.get(reverse('student_profile', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_student_course_home(self):
        res = self.client.get(reverse('student_course_home', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_student_course(self):
        res = self.client.get(reverse('student_course', args=[self.generate_random_str(5), random.randint(1,10)]))
        self.assertEqual(res.status_code, 302)

    def test_show_material(self):
        res = self.client.get(reverse('show_material', args=[self.generate_random_str(5), 1, self.generate_random_str(10)]))
        self.assertEqual(res.status_code, 302)

    def test_student_result_home(self):
        res = self.client.get(reverse('student_result_home', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_student_result(self):
        res = self.client.get(reverse('student_result', args=[self.generate_random_str(5), random.randint(1,10)]))
        self.assertEqual(res.status_code, 302)

    def test_student_performance_home(self):
        res = self.client.get(reverse('student_performance_home', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_student_performance(self):
        res = self.client.get(reverse('student_performance', args=[self.generate_random_str(5), random.randint(1,10)]))
        self.assertEqual(res.status_code, 302)

    def test_student_notice_home(self):
        res = self.client.get(reverse('student_notice_home', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_notice_view(self):
        res = self.client.get(reverse('notice_view', args=[self.generate_random_str(5), random.randint(1,10)]))
        self.assertEqual(res.status_code, 302)

    def test_student_fee_details_home(self):
        res = self.client.get(reverse('student_fee_details_home', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_student_fee_details_mess(self):
        res = self.client.get(reverse('student_fee_details_mess', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_student_fee_details_tuition(self):
        res = self.client.get(reverse('student_fee_details_tuition', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_student_fee_details_fine(self):
        res = self.client.get(reverse('student_fee_details_fine', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_student_timetable(self):
        res = self.client.get(reverse('student_timetable', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_student_timetable_exam(self):
        res = self.client.get(reverse('student_timetable_exam', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_student_timetable_class(self):
        res = self.client.get(reverse('student_timetable_class', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_student_certificate_request(self):
        res = self.client.get(reverse('student_certificate_request', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_student_create_request(self):
        res = self.client.get(reverse('student_create_request', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_student_view_request(self):
        res = self.client.get(reverse('student_view_request', args=[self.generate_random_str(5), random.randint(1,10)]))
        self.assertEqual(res.status_code, 302)

    def test_faculty(self):
        res = self.client.get(reverse('faculty'))
        self.assertEqual(res.status_code, 302)

    def test_faculty_home(self):
        res = self.client.get(reverse('faculty_home', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_faculty_profile(self):
        res = self.client.get(reverse('faculty_profile', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_faculty_course_home(self):
        res = self.client.get(reverse('faculty_course_home', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_faculty_course(self):
        res = self.client.get(reverse('faculty_course', args=[self.generate_random_str(5), random.randint(1,10)]))
        self.assertEqual(res.status_code, 302)

    def test_show_material(self):
        res = self.client.get(reverse('show_material', args=[self.generate_random_str(5), 1, self.generate_random_str(10)]))
        self.assertEqual(res.status_code, 302)

    def test_faculty_perf_home(self):
        res = self.client.get(reverse('faculty_perf_home', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_faculty_perf(self):
        res = self.client.get(reverse('faculty_perf', args=[self.generate_random_str(5), random.randint(1,10)]))
        self.assertEqual(res.status_code, 302)

    def test_faculty_notice_home(self):
        res = self.client.get(reverse('faculty_notice_home', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_notice_view(self):
        res = self.client.get(reverse('notice_view', args=[self.generate_random_str(5), random.randint(1,10)]))
        self.assertEqual(res.status_code, 302)

    def test_faculty_timetable(self):
        res = self.client.get(reverse('faculty_timetable', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_faculty_timetable_exam(self):
        res = self.client.get(reverse('faculty_timetable_exam', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_faculty_timetable_class(self):
        res = self.client.get(reverse('faculty_timetable_class', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_faculty_certificate_request(self):
        res = self.client.get(reverse('faculty_certificate_request', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_faculty_create_request(self):
        res = self.client.get(reverse('faculty_create_request', args=[self.generate_random_str(5)]))
        self.assertEqual(res.status_code, 302)

    def test_faculty_view_request(self):
        res = self.client.get(reverse('faculty_view_request', args=[self.generate_random_str(5), random.randint(1,10)]))
        self.assertEqual(res.status_code, 302)
