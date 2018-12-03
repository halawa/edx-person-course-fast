# MIT License
Copyright 2018, Sherif A. Halawa

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Getting Started
1. Make sure pip is up-to-date: `pip install --upgrade pip`
1. Installing Python requirements. `cd` into the software root directory, and then run pip install -r requirements.txt
If you are on python 3, this may be python -m pip install -r requirements.txt
Preferably, create a virtual environment (https://docs.python.org/3/tutorial/venv.html) to host your installation,
so installed package versions do not conflict with other versions possibly required by other python setups on your system.

2. Create a copy of settings.example.py, and place it in the same folder. Change its precisely to settings.py
Populate its parameters.
** Note: If you ever need to push changes upstream via pull requests, please double check that settings.py is ignored
by git and won't get pushed, because settings.py will probably contain database connection parameters. **

3. Create a copy of custom_utilities_example.py, and implement all functions in it. Please make sure you do not push
this file upstream, since it contains the functions that will likely differ from one open edX platform deployment to
another, such as fetching grades and course metadata.

4. If all config is correct, you should now be able to run any of the main_-------.py scripts as `python main_-------.py`
You can do a quick test run over 3 courses by switching on the "quick_run" parameter in your settings.py.

# Common Parameters
Some parameters are defined in the code that might affect certain analysis outputs. It is important to point them out
and unify them if the analysis is being run by different researchers.

These parameters are all placed in the settings file to ensure all parts of the analysis read their same values.
- min_enrollments_for_course_inclusion: This is used to filter out "playground courses", created for learning studio,
for instance. Analysis functions that loop over courses fetch a list of course IDs from the enrollments table, and exclude
the course if its number of enrollments is lower than this parameter.
- min_viewers_for_chapter_inclusion: This is used to filter out chapters that haven't gone live, based on how many
viewers viewed it.
