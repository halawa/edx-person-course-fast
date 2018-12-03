import os
import csv
import MySQLdb

from settings import SETTINGS


# --------------------- DB connections --------------------- #
def select(cur, query):
    cur.execute(query)
    return list(cur.fetchall())


def connect_to_db(p):
    con = MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['password'], db=p['db'], port=p['port'])
    cur = con.cursor(MySQLdb.cursors.DictCursor)
    select(cur, "SET CHARACTER SET utf8")
    return cur


def connect_to_lms():
    return connect_to_db(SETTINGS["connections"]["lms"])
# --------------------- End: DB connections --------------------- #


# --------------------- String utilities --------------------- #
def canonicalize_file_name(name):
    replace_chars = "/+:"
    for c in replace_chars:
        name = name.replace(c, "_")
    return name
# --------------------- End: String utilities --------------------- #


# --------------------- CSV utilities --------------------- #
def read_csv_as_dicts(file_path):
    # Assumes exactly 1 header row at the top.
    f = open(file_path)
    csv_reader = csv.reader(f)
    data = []
    header = None

    for ri, row in enumerate(csv_reader):
        if ri == 0:
            header = row
        else:
            data.append({header[i]: v for i, v in enumerate(row)})

    f.close()

    return header, data


def merge_csvs(file_paths, output_file_path, sep=","):
    # Assumes exactly 1 header row at the top of each file, and that all headers have the same fields.
    f_out = open(output_file_path, "w")
    csv_writer = csv.writer(f_out, delimiter=sep)
    common_header = None

    for fi, fp in enumerate(file_paths):
        header, data = read_csv_as_dicts(fp)
        if fi == 0:
            common_header = header
            csv_writer.writerow(header)
        rows = [
            [d[field] for field in common_header] for d in data
        ]
        csv_writer.writerows(rows)

    f_out.close()
# --------------------- End: CSV utilities --------------------- #


# --------------------- Fetch list of course IDs --------------------- #
def get_course_ids():
    # Get the list of courses with substantial enrollments
    cur_lms = connect_to_lms()
    q = """
                SELECT course_id, COUNT(*) AS num_enr FROM student_courseenrollment
                GROUP BY course_id HAVING num_enr >= {};
            """.format(SETTINGS["min_enrollments_for_course_inclusion"])
    course_enrollment_counts = select(cur_lms, q)
    course_ids = [row['course_id'] for row in course_enrollment_counts]
    if SETTINGS["quick_run"]:
        course_ids = course_ids[:3]

    return [c for c in course_ids if c not in SETTINGS["excluded_course_ids"]]
# --------------------- Fetch list of course IDs --------------------- #

# --------------------- Create results directory --------------------- #
def create_results_dir():
    if not os.path.exists(SETTINGS["results_path"]):
        os.makedirs(SETTINGS["results_path"])
# --------------------- End: Create results directory --------------------- #
