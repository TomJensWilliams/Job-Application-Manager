import os
import sys

def file_exists(file):
    return os.path.isfile(file)

def directory_exists(directory):
    return os.path.isdir(directory)

def directory_is_empty(directory):
    return not any(os.scandir(directory))

def delete_file_if_found(file):
    if file_exists(file):
        os.remove(file)

def delete_empty_directory_if_found(directory):
    if directory_exists(directory) and directory_is_empty(directory):
        os.rmdir(directory)

def count_files(directory):
    count = 0
    for entry in os.scandir(directory):
        if entry.is_file():
            count += 1
    return count

def count_directories(directory):
    count = 0
    for entry in os.scandir(directory):
        if entry.is_dir():
            count += 1
    return count