from utilities import *
try:
    from custom_utilities import get_course_grade_data
except ImportError:
    from custom_utilities_example import get_course_grade_data


def get_course_file_path(course_id):
    return SETTINGS["results_path"] + canonicalize_file_name(course_id) + ".csv"


def get_course_data(course_id):
    cur_lms = connect_to_lms()

    # 1. Get the number of chapters in the course
    q = """
        SELECT module_id, COUNT(*) AS num_eng FROM courseware_studentmodule
        WHERE module_type='chapter' AND course_id='{}'
        GROUP BY module_id HAVING num_eng >= {}
    """.format(course_id, SETTINGS["min_viewers_for_chapter_inclusion"])
    chapters = select(cur_lms, q)
    num_chapters = len(chapters)

    # 2. Get enrollments
    q = """
        SELECT user_id, email, gender, country, level_of_education, year_of_birth
        FROM student_courseenrollment JOIN auth_userprofile USING(user_id)
        JOIN auth_user ON auth_user.id=auth_userprofile.user_id
        WHERE course_id='{}'
    """.format(course_id)
    enrollments = select(cur_lms, q)

    # 3. Get engagement record for each student
    q = """
        SELECT * FROM (

            SELECT student_id, COUNT(*) AS num_ix FROM courseware_studentmodule
            WHERE course_id='{}'
            GROUP BY student_id

        ) AS t1 JOIN (

            SELECT student_id, COUNT(*) AS num_chapters FROM courseware_studentmodule
            WHERE course_id='{}' AND module_type='chapter'
            GROUP BY student_id

        ) AS t2 USING(student_id)
    """.format(course_id, course_id)
    eng_data = select(cur_lms, q)
    eng_dict = {r['student_id']: r for r in eng_data}

    # 4. Get grades data
    course_grades = get_course_grade_data(course_id)

    # 5. Merge in fields together
    for enrollment in enrollments:
        user_id = enrollment['user_id']
        enrollment['viewed'] = 0
        enrollment['explored'] = 0
        enrollment['completed'] = False
        enrollment['grade'] = 0

        if user_id in course_grades:
            enrollment['completed'] = course_grades[user_id]["completed"]
            enrollment['grade'] = course_grades[user_id]["grade"]

        if user_id in eng_dict:
            enrollment['viewed'] = int(eng_dict[user_id]['num_ix'] > 0)
            enrollment['explored'] = int(eng_dict[user_id]['num_chapters'] >= 0.5 * num_chapters)

    # 4. Write out into the course's csv file
    course_file_path = get_course_file_path(course_id)
    f = open(course_file_path, "w")
    csvw = csv.writer(f)
    header = [
        "course_id", "user_id", "completed", "cc_by_ip", "loe", "yob", "gender", "grade", "viewed", "explored",
        "certified"
    ]
    csvw.writerow(header)
    for enrollment in enrollments:
        csvw.writerow([
            course_id,
            enrollment["user_id"],
            enrollment["completed"],
            enrollment["country"],
            enrollment["level_of_education"],
            enrollment["year_of_birth"],
            enrollment["gender"],
            enrollment["grade"],
            enrollment["viewed"],
            enrollment["explored"],
            False,
        ])

    f.close()


def main():
    print("---")
    print("Starting generation of all course person data file")
    # Ensure that the results directory exists
    create_results_dir()
    course_ids = get_course_ids()

    # 1. Loop to fetch data course by course
    file_paths = []
    for course_id in course_ids:
        print("\t Generating for course: " + course_id)

        course_file_path = get_course_file_path(course_id)
        file_paths.append(course_file_path)

        if not os.path.exists(course_file_path):
            get_course_data(course_id)

    # 3. Merge CSVs into 1
    output_file_path = SETTINGS["results_path"] + "all_courses.csv"
    merge_csvs(file_paths, output_file_path)

    print("Generated successfully. Please find it as \"all_courses.csv\" in the results directory specified in your \
settings.py")
    print("---")


if __name__ == "__main__":
    main()
