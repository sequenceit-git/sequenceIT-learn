from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views import defaults as default_views
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog
from django.http import JsonResponse
from django.views.generic import RedirectView

def temporary_seed_db(request):
    if not request.user.is_superuser:
        return JsonResponse({"status": "error", "message": "Permission denied. Superuser required."})
    try:
        import random
        from django.utils import timezone
        from core.models import Session, Semester, NewsAndEvents, ActivityLog
        from course.models import Program, Course, CourseAllocation, Upload, UploadVideo
        from accounts.models import User, Student, Parent

        print("--- Cleaning up existing database records ---")
        Semester.objects.all().delete()
        Session.objects.all().delete()
        CourseAllocation.objects.all().delete()
        Course.objects.all().delete()
        Program.objects.all().delete()
        Student.objects.all().delete()
        Parent.objects.all().delete()
        User.objects.filter(is_superuser=False, is_staff=False).delete()
        NewsAndEvents.objects.all().delete()
        ActivityLog.objects.all().delete()

        print("--- Seeding Sessions and Semesters ---")
        sessions = []
        for year in range(2023, 2027):
            session_name = f"{year}/{year+1}"
            is_current = (year == 2025)
            s = Session.objects.create(
                session=session_name,
                is_current_session=is_current,
                next_session_begins=timezone.now().date() + timezone.timedelta(days=365)
            )
            sessions.append(s)

        semesters = []
        for s in sessions:
            for sem_name in ["First", "Second", "Third"]:
                is_current = (s.is_current_session and sem_name == "First")
                sem = Semester.objects.create(
                    semester=sem_name,
                    is_current_semester=is_current,
                    session=s,
                    next_semester_begins=timezone.now().date() + timezone.timedelta(days=120)
                )
                semesters.append(sem)

        print("--- Seeding Programs ---")
        programs_data = [
            ("Computer Science & Engineering", "Core study of computation, programming languages, and algorithms."),
            ("Electrical & Electronics Engineering", "Focus on power systems, analog circuits, and electronics."),
            ("Mechanical Engineering", "Mechanics, thermodynamics, and structural engineering studies."),
            ("Civil Engineering", "Infrastructure design, structural mechanics, and hydraulics."),
            ("Business Administration", "Modern corporate management, marketing, and finance foundations."),
            ("Information Technology", "System administration, cloud computing, and databases.")
        ]
        programs = []
        for title, summary in programs_data:
            p = Program.objects.create(title=title, summary=summary)
            programs.append(p)

        print("--- Seeding Courses ---")
        courses_data = [
            ("Introduction to Programming", "CSE101", 3),
            ("Data Structures & Algorithms", "CSE201", 4),
            ("Database Management Systems", "CSE301", 3),
            ("Web Application Development", "CSE302", 3),
            ("Artificial Intelligence", "CSE401", 4),
            ("Basic Electrical Engineering", "EEE101", 3),
            ("Digital Electronics", "EEE201", 3),
            ("Engineering Mechanics", "ME101", 3),
            ("Strength of Materials", "ME201", 3),
            ("Principles of Management", "MGT101", 3),
            ("Financial Accounting", "ACC101", 3),
            ("Network Security", "IT402", 3)
        ]
        courses = []
        for title, code, credit in courses_data:
            p = random.choice(programs)
            c = Course.objects.create(
                title=title,
                code=code,
                slug=code.lower(),
                credit=credit,
                summary=f"This course covers core concepts of {title}.",
                program=p,
                level=random.choice(["Beginner", "Intermediate", "Advanced"]),
                year=random.randint(1, 4),
                semester=random.choice(["First", "Second", "Third"]),
                is_elective=random.choice([True, False])
            )
            courses.append(c)

        print("--- Seeding Lecturers ---")
        lecturer_names = [
            ("Alice", "Smith"),
            ("Bob", "Johnson"),
            ("Charlie", "Williams"),
            ("Diana", "Brown"),
            ("Edward", "Davis")
        ]
        lecturers = []
        for first, last in lecturer_names:
            username = f"{first.lower()}_{random.randint(100, 999)}"
            u = User.objects.create_user(
                username=username,
                first_name=first,
                last_name=last,
                email=f"{first.lower()}@sequenceit.com",
                phone=f"+1-555-01{random.randint(10, 99)}",
                address=f"Room {random.randint(101, 404)}, Science Building",
                is_lecturer=True
            )
            lecturers.append(u)

        print("--- Seeding Students ---")
        student_names = [
            ("John", "Doe"), ("Jane", "Doe"), ("Michael", "Green"), ("Emily", "White"),
            ("David", "Black"), ("Sarah", "Blue"), ("James", "Taylor"), ("Emma", "Thomas"),
            ("Daniel", "Jackson"), ("Olivia", "Martin"), ("William", "Lee"), ("Sophia", "Perez"),
            ("Lucas", "Thompson"), ("Mia", "Garcia"), ("Alexander", "Martinez"), ("Isabella", "Robinson")
        ]
        students = []
        for first, last in student_names:
            username = f"{first.lower()}_{random.randint(1000, 9999)}"
            u = User.objects.create_user(
                username=username,
                first_name=first,
                last_name=last,
                email=f"{first.lower()}.{last.lower()}@sequenceit.com",
                phone=f"+1-555-02{random.randint(10, 99)}",
                address=f"Student Housing Block {random.choice(['A', 'B', 'C'])}",
                is_student=True
            )
            s = Student.objects.create(
                student=u,
                level=random.choice(["100", "200", "300", "400"]),
                program=random.choice(programs)
            )
            students.append(s)

        print("--- Seeding Parents ---")
        parent_names = [
            ("Robert", "Doe"), ("Patricia", "White"), ("Thomas", "Green"), ("Barbara", "Black"), ("Mark", "Taylor")
        ]
        for first, last in parent_names:
            username = f"{first.lower()}_{random.randint(100, 999)}"
            u = User.objects.create_user(
                username=username,
                first_name=first,
                last_name=last,
                email=f"{first.lower()}@parent.com",
                phone=f"+1-555-03{random.randint(10, 99)}",
                address=f"Suburban Area, City",
                is_parent=True
            )
            s = random.choice(students)
            Parent.objects.create(
                user=u,
                student=s,
                first_name=first,
                last_name=last,
                phone=u.phone,
                email=u.email,
                relation_ship=random.choice(["Father", "Mother", "Guardian"])
            )

        print("--- Seeding Course Allocations ---")
        for l in lecturers:
            current_session = next((s for s in sessions if s.is_current_session), sessions[-1])
            alloc = CourseAllocation.objects.create(
                lecturer=l,
                session=current_session
            )
            alloc.courses.set(random.sample(courses, random.randint(2, 4)))

        print("--- Seeding Uploads and Videos ---")
        for c in courses:
            for i in range(random.randint(1, 2)):
                Upload.objects.create(
                    title=f"Lecture notes {i+1} on {c.title}",
                    course=c,
                    file="uploads/sample_notes.pdf"
                )
            UploadVideo.objects.create(
                title=f"Video Tutorial: Introduction to {c.title}",
                slug=f"intro-to-{c.slug}-{random.randint(10, 99)}",
                course=c,
                video="uploads/sample_video.mp4",
                summary=f"This video covers introductory concepts for {c.title}."
            )

        print("--- Seeding News and Events ---")
        news_titles = [
            ("SequenceIT Fall Semester Registration Open", "Registration for the upcoming semester is now open. Make sure to complete your registration by the deadline.", "News"),
            ("Annual Engineering Fair 2026", "Join us for the annual engineering exhibition showcasing student innovation and research projects.", "Event"),
            ("Guest Lecture: Advances in AI and Machine Learning", "Dr. Alan Turing Jr. will be speaking about the future of deep learning models in education.", "Event"),
            ("New Student Orientation Schedule", "Welcome to all new students! Please check the orientation guide and attend the welcome session on Monday.", "News"),
            ("Library Extended Study Hours during Exams", "The library will be open 24/7 during the final exam week. Study rooms can be reserved online.", "News"),
            ("Sports Week 2026 Registration", "Sign up now for basketball, soccer, and table tennis tournaments starting next month.", "Event")
        ]
        for title, summary, posted_as in news_titles:
            NewsAndEvents.objects.create(
                title=title,
                summary=summary,
                posted_as=posted_as
            )

        print("--- Seeding Activity Logs ---")
        log_messages = [
            "User admin registered a new student user.",
            "Course EEE101 allocated to lecturer Bob Johnson.",
            "Uploaded new syllabus PDF for Web Application Development.",
            "New announcement posted: Annual Engineering Fair 2026.",
            "Student grade result updated for CSE201.",
            "System backup completed successfully.",
            "Added a new post to News & Events."
        ]
        for msg in log_messages:
            ActivityLog.objects.create(message=msg)

        return JsonResponse({"status": "success", "message": "Database seeded successfully with premium test data!"})
    except Exception as e:
        import traceback
        return JsonResponse({"status": "error", "message": str(e), "traceback": traceback.format_exc()})

admin.site.site_header = "Learn With SequenceIT Admin"

urlpatterns = [
    path("", RedirectView.as_view(url="/en/", permanent=False)),  # root redirect to default locale
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("seed-db/", temporary_seed_db),
    # Fallback: non-i18n /accounts/login/ redirect to /en/accounts/login/
    path("accounts/login/", RedirectView.as_view(url="/en/accounts/login/", permanent=False)),
    path("accounts/", RedirectView.as_view(url="/en/accounts/login/", permanent=False)),
]

urlpatterns += i18n_patterns(
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("", include("core.urls")),
    path("jet/", include("jet.urls", "jet")),  # Django JET URLS
    path(
        "jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")
    ),  # Django JET dashboard URLS
    path("accounts/", include("accounts.urls")),
    path("programs/", include("course.urls")),
    path("result/", include("result.urls")),
    path("search/", include("search.urls")),
    path("quiz/", include("quiz.urls")),
    path("payments/", include("payments.urls")),
)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
