from django.template.defaultfilters import register

def sort_list(a_list, attribute):
    a_list.sort(key=lambda x: getattr(x, attribute))
    return a_list

@register.filter
def sort_files_by_name(file_list):
    """ Sorts a list of files by their "original_filename" attribute.
    It is intended for sorting lists of filer files"""
    file_list = list(file_list)
    return sort_list(file_list, "original_filename")

@register.filter
def sort_folders_by_name(folder_list):
    """ Sorts a list of files by their "name" attribute.
    It is intended for sorting lists of filer files"""
    folder_list = list(folder_list)
    return sort_list(folder_list, "name")