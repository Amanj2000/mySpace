from django.contrib import admin
from django.urls import path, include
from mySpace_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),

    #Student URLs
    path('student', views.student, name="student"),
    path('student/<str:username>', views.student_home, name="student_home"),
    path('student/<str:username>/profile', views.student_profile, name="student_profile"),
    
    path('student/<str:username>/result', views.student_result_home, name="student_result_home"),
    path('student/<str:username>/result/<int:sem>', views.student_result, name="student_result"),

    path('student/<str:username>/perf', views.student_perf_home, name="student_performance_home"),
    path('student/<str:username>/perf/<int:course_id>', views.student_perf, name="student_performance"),

    path('student/<str:username>/notice', views.student_notice_home, name="student_notice_home"),
    path('student/<str:username>/notice/<int:notice_id>', views.student_notice, name="student_notice_read"),

    path('student/<str:username>/fee-payment', views.student_fee_payment_home, name="student_fee_details_home"),
    path('student/<str:username>/fee-payment/mess', views.student_fee_payment_mess, name="student_fee_details_mess"),
    path('student/<str:username>/fee-payment/tuition', views.student_fee_payment_tuition, name="student_fee_details_tuition"),

    #Faculty URLs
    path('faculty', views.faculty, name="faculty"),
    path('faculty/<str:username>', views.faculty_home, name="faculty_home"),
    path('faculty/<str:username>/profile', views.faculty_profile, name="faculty_profile"),

]
