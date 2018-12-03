
SETTINGS = {
    "quick_run": False,  # To test things out, set this to True. It will limit the analysis to 3 courses
    "results_path": "",  # The path on your system where result files will be placed
    "excluded_course_ids": [],
    "connections": {  # The database connection parameters
        "lms": {
            "db": "edxapp",
            "user": "root",
            "password": "",
            "host": "",
            "port": 3306,
        },
    },

    # Analysis hyper-parameters
    # --------------------------
    "min_enrollments_for_course_inclusion": 50,
    "min_viewers_for_chapter_inclusion": 15,
}
