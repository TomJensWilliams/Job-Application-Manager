import json
from interface_functions import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~ Helpful Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def conditional_remove(input, values, /):
    output = input
    for value in values:
        if value in output:
            output.remove(value)
    return output

def conditional_append(input, values, /):
    output = input
    for value in values:
        if not value in output:
            output.append(value)
    return output

def append_if_true(input, values, boolean, /):
    output = input
    for value in values:
        if boolean:
            output.append(value)
    return output

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~ Input Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def choose_from_options(prompt, options, /, *, option_choice="options", exit_choice="exit"):
    while True:
        user_input = input(prompt + f"\n(To see all options enter \"{option_choice}\",\nTo exit enter \"{exit_choice}\"):\t")
        if user_input == exit_choice:
            return exit_choice
        elif user_input == option_choice:
            print(f"Options: {' '.join(conditional_remove(options, [option_choice, exit_choice]))}\n")
        elif user_input in options:
            return user_input
        else:
            print("That is not an available option.\n")

def choose_multiple_from_options(prompt, options, /, *, option_choice="options", exit_choice="exit"):
    output = []
    while True:
        user_input = choose_from_options(prompt, conditional_remove(options, output), option_choice = option_choice, exit_choice=exit_choice)
        if user_input == exit_choice:
            break
        else:
            output.append(user_input)
    return output

def free_user_input(prompt, /, *, exit_choice="exit"):
    return input(prompt + f"\n(To exit enter \"{exit_choice}\"):\t")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~ Handling Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# ADD QUIT OPTIONS?

def handle_create(database, table, /, *, print_statements=False):
    input_style = choose_from_options("Would you like to create a record manually or using a file?", ["manually", "file"])
    if input_style == "exit":
        return
    if input_style == "manually":
        fields = read_fields(database, table, rowid=False, print_statements=print_statements)
        user_input = []
        for field in fields:
            value_input = free_user_input(f"What value would you like to enter for {field}?")
            if value_input == "exit":
                return # break?
            else:
                user_input.append(value_input)
        create_record(database, table, fields, user_input, print_statements=print_statements)
    if input_style == "file":
        filename = free_user_input("What is the name of the file?\nPlease remember the file ending:\t")
        if filename == "exit":
            return
        else:
            with open(f"../input/{filename}", "r") as f:
                file_contents = json.loads(f.read())
                create_record(database, table, file_contents["fields"], file_contents["values"], print_statements=print_statements)

def handle_read(database, table, /, *, rowid=False, print_statements=False):
    input_style = choose_from_options("Would you like to read a record manually or using a file?", ["manually", "file"])
    if input_style == "exit":
        return
    elif input_style == "manually":
        fields = read_fields(database, table, rowid=rowid, print_statements=print_statements)
        selection_choice = choose_from_options("Would you like to read all fields or only some?", ["all", "some"])
        if selection_choice == "exit":
            return
        elif selection_choice == "all":
            input_selections = None
        elif selection_choice == "some":
            input_selections = choose_multiple_from_options("Which field would you like to add to be read?", fields)
            if len(input_selections) == 0:
                return
        fields_choice = choose_from_options("Would you like to limit the records read by field values?", ["yes", "no"])
        if fields_choice== "exit":
            return
        elif fields_choice == "yes":
            input_fields = choose_multiple_from_options("Which field would you like to add to be checked?", fields)
            if len(input_fields) == 0:
                return
            else:
                input_values = []
                for field in input_fields:
                    value_choice = free_user_input(f"What value would you like to check for {field}?")
                    if value_choice == "exit":
                        return # continue?
                    else:
                        input_values.append(value_choice)
            """
            while True:
                field_choice = choose_from_options("Which field would you like to add to be checked?", conditional_remove_multiple(fields, input_fields))
                if field_choice == "exit":
                    break
                else:
                    input_fields.append(field_choice)
                value_choice = free_user_input(f"What value would you like to check for {field_choice}?")
                if value_choice == "exit":
                    continue
                else:
                    input_values.append(value_choice)
            if len(field_choice) == 0:
                return
            """
        elif fields_choice == "no":
            input_fields = None
            input_values = None
        print(read_records(database, table, rowid=rowid, selections=input_selections, fields=input_fields, values=input_values, print_statements=print_statements))
    elif input_style == "file":
        filename = free_user_input("What is the name of the file?\nPlease remember the file ending:\t")
        if filename == "exit":
            return
        else:
            with open(f"../input/{filename}", "r") as f:
                file_contents = json.loads(f.read())
                print(read_records(database, table, rowid=rowid, selections=file_contents["selections"], fields=file_contents["fields"], values=file_contents["values"], print_statements=print_statements))

def handle_update(database, table, /, *, rowid=False, print_statements=False):
    input_style = choose_from_options("Would you like to read a record manually or using a file?", ["manually", "file"])
    if input_style == "exit":
        return
    elif input_style == "manually":
        fields = read_fields(database, table, rowid=rowid, print_statements=print_statements)
        """
        update_fields = []
        update_values = []
        match_fields = []
        match_values = []
        """
        update_fields = choose_multiple_from_options("Which field would you like to add to be set?", fields)
        if len(update_fields) == 0:
            return
        else:
            update_values = []
            for field in update_fields:
                value_choice = free_user_input(f"What value would you like to set for {field}?")
                if value_choice == "exit":
                    return
                else:
                    update_values.append(value_choice)
        """
        while True:
            field_choice = choose_from_options("Which field would you like to add to be set?", conditional_remove_multiple(fields, update_fields))
            if field_choice == "exit":
                break
            else:
                update_fields.append(field_choice)
            value_choice = free_user_input(f"What value would you like to set for {field_choice}?")
            if value_choice == "exit":
                continue
            else:
                update_values.append(value_choice)
        if len(field_choice) == 0:
            return
        """
        fields_choice = choose_from_options("Would you like to limit the records read by field values?", ["yes", "no"])
        if fields_choice == "exit":
            return
        elif fields_choice == "yes":
            match_fields = choose_multiple_from_options("Which field would you like to add to be set?", fields)
            if len(match_fields) == 0:
                return
            else:
                match_values = []
                for field in match_fields:
                    value_choice = free_user_input(f"What value would you like to check for {field}?")
                    if value_choice == "exit":
                        return
                    else:
                        match_values.append(value_choice)
        elif fields_choice == "no":
            match_fields = None
            match_values = None
        """
        while True:
            field_choice = choose_from_options("Which field would you like to add to be checked?", conditional_remove_multiple(fields, match_fields))
            if field_choice == "exit":
                break
            else:
                match_fields.append(field_choice)
            value_choice = free_user_input(f"What value would you like to check for {field_choice}?")
            if value_choice == "exit":
                continue
            else:
                match_values.append(value_choice)
        if len(field_choice) == 0:
            return
        """
        update_records(database, table, update_fields, update_values, match_fields=match_fields, match_values=match_values, print_statements=print_statements)
    elif input_style == "file":
        filename = free_user_input("What is the name of the file?\nPlease remember the file ending:\t")
        if filename == "exit":
            return
        else:
            with open(f"../input/{filename}", "r") as f:
                file_contents = json.loads(f.read())
                update_records(database, table, file_contents["update_fields"], file_contents["update_values"], match_fields=file_contents["match_fields"], match_values=file_contents["match_values"], print_statements=print_statements)

def handle_delete(database, table, /, *, rowid=False, print_statements=False):
    input_style = choose_from_options("Would you like to read a record manually or using a file?", ["manually", "file"])
    if input_style == "exit":
        return
    elif input_style == "manually":

        fields = read_fields(database, table, rowid=rowid, print_statements=print_statements)
        
        fields_choice = choose_from_options("Would you like to limit the records to be deleted by field values?", ["yes", "no"])
        if fields_choice == "exit":
            return
        elif fields_choice == "no":
            double_check = choose_from_options(f"Are you completely sure that you would like to delete are records in {table}", ["yes", "no"])
            if double_check == "exit" or double_check == "no":
                return
            elif double_check == "yes":
                input_fields = None
                input_values = None
        elif fields_choice == "yes":

            input_fields = choose_multiple_from_options("Which field would you like to add to be checked?", fields)
            if len(input_fields) == 0:
                return
            else:
                input_values = []
                for field in input_fields:
                    value_choice = free_user_input(f"What value would you like to check for {field}?")
                    if value_choice == "exit":
                        return
                    else:
                        input_values.append(value_choice)
            """
            while True:
                field_choice = choose_from_options("Which field would you like to add to be checked?", conditional_remove_multiple(fields, input_fields))
                if field_choice == "exit":
                    break
                else:
                    input_fields.append(field_choice)
                value_choice = free_user_input(f"What value would you like to check for {field_choice}?")
                if value_choice == "exit":
                    continue
                else:
                    input_values.append(value_choice)
            if len(field_choice) == 0:
                return
            """
        delete_records(database, table, fields=input_fields, values=input_values, print_statements=print_statements)
    elif input_style == "file":
        filename = free_user_input("What is the name of the file?\nPlease remember the file ending:\t")
        if filename == "exit":
            return
        else:
            with open(f"../input/{filename}", "r") as f:
                file_contents = json.loads(f.read())
                delete_records(database, table, fields=file_contents["fields"], values=file_contents["values"], print_statements=print_statements)

def handle_print(database, table, /, *,  print_statements=False):
    filename = free_user_input("What would you like the filename of the printed file to be?\nPlease include the appropriate file ending.")
    if filename == "exit":
        return
    else:
        print_table(database, table, filename, print_statements=print_statements)

def handle_run(table, /, *,  print_statement=False):
    rowid_input = free_user_input("What is the rowid associated with the search you would like to run?")
    if rowid_input == "exit":
        return
    else:
        run_search(table, rowid_input, print_statements=print_statement)

def handle_prepare(table, /, *, print_statements=False):
    print("Currently preparing a search from a file is the only supported option")
    filename = free_user_input("What is the name of the file?\n Please remember the file ending:")
    if filename == "exit":
        return
    else:
        with open(f"../input/{filename}") as f:
            file_contents = json.loads(f.read())
            prepare_search(table, file_contents, print_statements=print_statements)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~ Main Loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

if __name__ == "__main__":
    databases = ["dictionaries", "jobs", "searches"]
    tables = ["glassdoor", "indeed", "linkedin", "monster", "ziprecruiter"]
    base_actions = ["create", "read", "update", "delete", "print"]
    search_actions = ["run", "prepare"]
    while True:
        database = choose_from_options("Which database would you like to perform an action on?", databases)
        if database == "exit":
            break
        table = choose_from_options("Which table would you like to perform an action in relation to?", tables)
        if table == "exit":
            continue
        action = choose_from_options("Which action would you like to perform?", append_if_true(base_actions, search_actions, database == "searches"))
        if action == "exit":
            continue
        elif action == "create":
            handle_create(database, table)
        elif action == "read":
            handle_read(database, table)
        elif action == "update":
            handle_update(database, table)
        elif action == "delete":
            handle_delete(database, table)
        elif  action == "print":
            handle_print(database, table)
        elif action == "run":
            handle_run(table)
        elif action == "prepare":
            handle_prepare(table)