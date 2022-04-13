from mySpace_app.models import Student, SecCanRead, StudPartOf

def notices_count(request):
    user = Student.objects.get(user=request.user)
    partOf = StudPartOf.objects.get(student=user)
    canRead = SecCanRead.objects.filter(section=partOf.section)

    return {'notices_count': len(canRead)}