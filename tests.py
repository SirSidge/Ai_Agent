from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# Get Files Info
"""print(get_files_info("calculator", "."))
print(get_files_info("calculator", "pkg"))
print(get_files_info("calculator", "/bin"))
print(get_files_info("calculator", "../"))
print(get_files_info("calculator", "main.py"))"""

# Get File Content
"""print(get_file_content("calculator", "lorem.txt"))
print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))"""

# Write File
"""print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))"""

# Run Python File
print(run_python_file("calculator", "main.py")) # should print the calculator's usage instructions
print(run_python_file("calculator", "main.py", ["3 + 5"])) # should run the calculator... which gives a kinda nasty rendered result
print(run_python_file("calculator", "tests.py"))
print(run_python_file("calculator", "../main.py")) # this should return an error
print(run_python_file("calculator", "nonexistent.py")) # this should return an error