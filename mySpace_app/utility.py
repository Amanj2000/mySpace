from .models import User, Faculty, Course, InstTeaches, StudTakes, InstOf, StudPartOf, Student

def factTeaches(user, course_id):
    user = Faculty.objects.get(user=user)
    course = Course.objects.get(id=course_id)

    #All stud that takes this course
    stud_course = set()
    for entry in StudTakes.objects.filter(course=course):
        stud_course.add(entry.student.user.id)

    #All student taught by this faculty
    inst_of = InstOf.objects.filter(faculty=user)
    stud_sec = set()
    for sec in inst_of:
        stud_sec.update([st.student.user.id for st in StudPartOf.objects.filter(section=sec.section)])

    #Student that study this course by this faculty
    stud_allowed = stud_sec & stud_course
    return course, stud_allowed

def getFaculty(user, course_id):
    user = Student.objects.get(user=user)
    course = Course.objects.get(id=course_id)
    stud_sec = StudPartOf.objects.get(student=user).section

    inst = set()
    for entry in InstOf.objects.filter(section=stud_sec):
        inst.add(entry.faculty)
    
    for entry in InstTeaches.objects.filter(course=course):
        if entry.faculty in inst:
            return entry
    return None