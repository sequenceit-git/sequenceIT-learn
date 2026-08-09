import os
import sys
import django

# Add workspace directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from scripts.generate_fake_accounts_data import generate_fake_accounts_data
from scripts.generate_fake_core_data import generate_fake_core_data
from scripts.generate_fake_data import generate_fake_course_data, populate_course_allocation

def main():
    print("--- Starting Database Seeding ---")
    
    print("\n1. Generating Core Session & Semester Data...")
    generate_fake_core_data(
        num_news_and_events=15,
        num_sessions=4,
        num_semesters=6,
        num_activity_logs=20
    )

    print("\n2. Generating Student, Parent & Program Data...")
    generate_fake_accounts_data(
        num_programs=6,
        num_students=25,
        num_parents=15
    )

    print("\n3. Generating Course, Uploads & Media Data...")
    generate_fake_course_data(
        num_programs=4,
        num_courses=20,
        num_course_allocations=8,
        num_uploads=12,
        num_upload_videos=10,
        num_course_offers=4
    )

    print("\n4. Populating Lecturer Course Allocations...")
    populate_course_allocation(num_allocations=8)

    print("\n--- Database Seeding Completed Successfully! ---")

if __name__ == "__main__":
    main()
