# tests for custom_filer
import os, sys
from django.conf import settings
from django.utils import unittest
from django.test import SimpleTestCase
from custom_filer import filer_monkeypatch as fmp
from filer.models.filemodels import File

# this is so we can import django stuff
if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class FakeFiler(object):
    RESOURCE_ICON_PATH = File.RESOURCE_ICON_PATH
    RESOURCE_URL_BASE = File.RESOURCE_URL_BASE
    RESOURCE_ICON_SIZES = File.RESOURCE_ICON_SIZES
    RESOURCE_DEFAULT_ICON_SIZE = File.RESOURCE_DEFAULT_ICON_SIZE
    RESOURCE_EXT_MAPPINGS = File.RESOURCE_EXT_MAPPINGS

    ext_to_url = fmp.ext_to_url
    ext_to_icon_path = fmp.ext_to_icon_path
    get_resource_icon_url = fmp.get_resource_icon_url

    def __init__(self, extension):
        self.extension = extension

class TestSequenceFunctions(SimpleTestCase):

    def setUp(self):
        self.fake = FakeFiler('doc')

    def test_ext_to_url(self):
        url = fmp.ext_to_url(self.fake, 'doc', '16x16')
        self.assertEqual(url, '%simg/mime/16x16/file_extension_doc.png' % settings.STATIC_URL)

    def test_ext_to_url_no_ext(self):
        url = fmp.ext_to_url(self.fake, None, '16x16')
        self.assertEqual(url, '%simg/mime/16x16/file_extension_unknown.png' % settings.STATIC_URL)

    def test_ext_to_icon_path(self):
        icon_path = fmp.ext_to_icon_path(self.fake, 'doc', '16x16')
        expected_icon_path = os.path.join(File.RESOURCE_ICON_PATH, '16x16/file_extension_doc.png')
        self.assertEqual(icon_path, expected_icon_path)

    def test_ext_to_icon_path_no_ext(self):
        icon_path = fmp.ext_to_icon_path(self.fake, None, '16x16')
        expected_icon_path = os.path.join(File.RESOURCE_ICON_PATH, '16x16/file_extension_unknown.png')
        self.assertEqual(icon_path, expected_icon_path)

    def test_get_resource_icon_url_32(self):
        url = fmp.get_resource_icon_url_32(self.fake)
        self.assertEqual(url, '%simg/mime/32x32/file_extension_doc.png' % settings.STATIC_URL)

    def test_get_resource_icon_url_16(self):
        url = fmp.get_resource_icon_url_16(self.fake)
        self.assertEqual(url, '%simg/mime/16x16/file_extension_doc.png' % settings.STATIC_URL)

    def test_get_resource_icon_url_bad_size(self):
        url = fmp.get_resource_icon_url(self.fake, '16x32')
        self.assertEqual(url, '%simg/mime/32x32/file_extension_doc.png' % settings.STATIC_URL)

    def test_get_resource_icon_url_mapping(self):
        self.fake.extension = 'docx'
        url = fmp.get_resource_icon_url(self.fake, '32x32')
        self.assertEqual(url, '%simg/mime/32x32/file_extension_doc.png' % settings.STATIC_URL)

    def test_get_resource_icon_unknown_type(self):
        self.fake.extension = 'vimrc'
        url = fmp.get_resource_icon_url(self.fake, '32x32')
        self.assertEqual(url, '%simg/mime/32x32/file_extension_unknown.png' % settings.STATIC_URL)

if __name__ == '__main__':
    unittest.main()

