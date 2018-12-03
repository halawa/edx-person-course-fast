
def get_course_grade_data(course_id):
    """
    *** Please override this function in a file called custom_utilities.py, with the same call signature. ***

    Given a course ID, this function should return a dictionary keyed by user ID for the users in the course.
    Each user's value should be a dict with the keys:
      - grade: The user's grade in the course
      - completed: A boolean indicating whether the student completed the course.

    Example of output format:
        {
            1980032: {"grade": 0.74, "completed": True},
            1981432: {"grade": 0.24, "completed": False},
            .
            .
            .
        }

    :param course_id: ID for course to fetch grade data for.
    :return: Dictionary
    """

    raise NotImplementedError("The function get_course_grade_data is not implemented. \
    Please create a file called custom_utilities.py and implement this function with the same call signature in it.")


def get_course_metadata():
    """
    *** Please override this function in a file called custom_utilities.py, with the same call signature. ***

    Generate the course metadata required by the analysis for all courses. The output is a dict, keyed by course ID.
    Each course's value is a

    :return: A dict, where each key is a course ID, and the value is a dict with fields
        - "course_id",
        - "semester",
        - "course_launch",
        - "4-way"
    """
