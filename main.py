from backend.controllers.file_access import file_path, all_files
from backend.controllers.user_inputs import get_file_name, option_selection


def main():
    file_name = get_file_name()
    user_selection = option_selection(file_name)

if __name__ == "__main__":
    main()


# Functions under 20-30 lines of code

# Similar functions grouped under file. Like all inputs in input.py

# Max 200 ish lines in one file