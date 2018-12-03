from utilities import *
from main_person_course_data import main as generate_person_course_data

try:
    from custom_utilities import get_course_metadata
except ImportError:
    from custom_utilities_example import get_course_metadata


def main():
    print("---")
    print("Starting generation of course metadata file ...")

    # Ensure that the results directory exists
    create_results_dir()
    course_ids = get_course_ids()

    # 1. Generate the course metadata file
    all_course_metadata = get_course_metadata()

    courses_without_metadata = [course_id for course_id in course_ids if course_id not in all_course_metadata]
    if len(courses_without_metadata) > 0:
        print("""
Error: Some courses have no metadata entries. Consider:
   - Addressing the cases for courses that should be included in the analysis in your get_course_metadata function.
   - Adding courses that shouldn't be included in the analysis to the \"excluded_course_ids\" setting in settings.py

List of courses with no metadata:
{}""".format(courses_without_metadata))
        return

    output_file_path = SETTINGS["results_path"] + "course_metadata.csv"
    f = open(output_file_path, "w")
    csvw = csv.writer(f, delimiter=",")
    header = ["semester", "course_launch", "course_id", "4-way"]
    rows = [header]
    for course_id in course_ids:
        metadata = all_course_metadata[course_id]
        rows.append([metadata[k] for k in header])
    csvw.writerows(rows)

    print("Generated successfully. Please find it in the results directory specified in your settings.py")
    print("---")

    # 2. Run the course-person data file generator
    generate_person_course_data()


if __name__ == "__main__":
    main()
