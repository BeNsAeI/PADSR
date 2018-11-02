import os

def check_dir_write_access(filename):
    '''
    Check if a directory where a file is located is accessible for writing,

    filename: string - the name of file to check. Can be a relative/absolute path
    return: True if dir is available for writing, False otherwise
    '''
    if not filename:
        return False
    out_dir = os.path.dirname(filename) or '.'
    return os.access(out_dir, os.W_OK)

def check_file_exists(filename):
    '''
    Check if file is accessible for reading.

    filename: string - the name of file to check. Can be a relative/absolute path
    return: True if file exists and available for reading, False otherwise
    '''
    if not filename:
        return False
    return os.access(filename, os.R_OK)


