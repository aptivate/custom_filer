from django_dynamic_fixture import G
from resources.models import TrainingCourse
from filer.models.foldermodels import Folder
from filer.models.filemodels import File
from django.test.testcases import TestCase
from custom_filer.templatetags.file_folder_sorting import sort_files_by_name,\
    sort_folders_by_name

class SortingTagTests(TestCase):
    training_course = None
    files = None
    
    def setUp(self):
        main_directory = G(Folder)
        self.files = []
        self.training_course = G(TrainingCourse, training_root=main_directory,
                                 ignore_fields=["image"])
        i = 1
        j = 1
        for _ in range(3):
            directory = G(Folder, parent=main_directory, name=i)
            i += 1
            for _ in range(5):
                self.files.append(
                  G(File, folder=directory, original_filename=j))
                j += 1
            
    
    def test_files_in_a_folder_are_sorted_into_alphabetical_order(self):
        actual_files = self.files
        files = self.files[:]
        files[0], files[1] = files[1], files[0]
        expected_files = sort_files_by_name(files)
        
        self.assertListEqual(actual_files, expected_files)
    
    def test_folders_are_sorted_into_alphabetical_order(self):
        expected_folders = \
            list(self.training_course.training_root.get_children())
        folders = expected_folders[:]
        folders[0], folders[1] = folders[1], folders[0]
        actual_folders = sort_folders_by_name(folders)
        self.assertListEqual(expected_folders, actual_folders)