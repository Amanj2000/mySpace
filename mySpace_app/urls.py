from django.contrib import admin
from django.urls import path, include
from mySpace_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    #Student URLs
    path('student/', views.student, name="student"),
    path('student/<str:username>/', views.student_home, name="student_home"),
    path('student/<str:username>/profile/', views.student_profile, name="student_profile"),

    path('student/<str:username>/course/', views.student_course_home, name="student_course_home"),

    path('student/<str:username>/result/', views.student_result_home, name="student_result_home"),
    path('student/<str:username>/result/<int:sem>/', views.student_result, name="student_result"),

    path('student/<str:username>/perf/', views.student_perf_home, name="student_performance_home"),
    path('student/<str:username>/perf/<int:course_id>/', views.student_perf, name="student_performance"),

    path('student/<str:username>/notice/', views.student_notice_home, name="student_notice_home"),
    path('student/<str:username>/notice/<int:notice_id>/', views.notice_view, name="notice_view"),

    path('student/<str:username>/fee-payment/', views.student_fee_payment_home, name="student_fee_details_home"),
    path('student/<str:username>/fee-payment/mess/', views.student_fee_payment_mess, name="student_fee_details_mess"),
    path('student/<str:username>/fee-payment/tuition/', views.student_fee_payment_tuition, name="student_fee_details_tuition"),
    path('student/<str:username>/fee-payment/fine/', views.student_fee_payment_fine, name="student_fee_details_fine"),

    path('student/<str:username>/timetable/', views.timetable, name="student_timetable"),
    path('student/<str:username>/timetable/exam/', views.timetable_exam, name="student_timetable_exam"),
    path('student/<str:username>/timetable/class/', views.timetable_class, name="student_timetable_class"),

    path('student/<str:username>/cert-req/', views.cert_req_home, name="student_certificate_request"),
    path('student/<str:username>/cert-req/new/', views.cert_req_new, name="student_create_request"),
    path('student/<str:username>/cert-req/<int:cert_id>/', views.cert_req_view, name="student_view_request"),

    #Faculty URLs
    path('faculty/', views.faculty, name="faculty"),
    path('faculty/<str:username>/', views.faculty_home, name="faculty_home"),
    path('faculty/<str:username>/profile/', views.faculty_profile, name="faculty_profile"),

    path('faculty/<str:username>/courses/', views.faculty_course_home, name="faculty_course_home"),
    path('faculty/<str:username>/courses/<int:course_id>/', views.faculty_course_perf, name="faculty_course_perf"),

    path('faculty/<str:username>/notice/', views.faculty_notice_home, name="faculty_notice_home"),
    path('faculty/<str:username>/notice/publish/', views.faculty_notice_publish, name="faculty_notice_publish"),
    path('faculty/<str:username>/notice/edit/<int:notice_id>/', views.faculty_notice_edit, name="faculty_notice_edit"),
    path('faculty/<str:username>/notice/<int:notice_id>/', views.notice_view, name="notice_view"),

    path('faculty/<str:username>/timetable/', views.timetable, name="faculty_timetable"),
    path('faculty/<str:username>/timetable/exam/', views.timetable_exam, name="faculty_timetable_exam"),
    path('faculty/<str:username>/timetable/class/', views.timetable_class, name="faculty_timetable_class"),

    path('faculty/<str:username>/cert-req/', views.cert_req_home, name="faculty_certificate_request"),
    path('faculty/<str:username>/cert-req/new/', views.cert_req_new, name="faculty_create_request"),
    path('faculty/<str:username>/cert-req/<int:cert_id>/', views.cert_req_view, name="faculty_view_request")
]
