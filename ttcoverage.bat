coverage run --source bowl -m unittest discover -s tests -p "*_tests.py"
rem coverage report
coverage html
start chrome htmlcov\index.html

