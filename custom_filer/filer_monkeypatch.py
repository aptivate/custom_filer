import os
from django.conf import settings
from filer.models.filemodels import File

File.RESOURCE_URL_BASE = os.path.join(settings.STATIC_URL, 'img', 'mime')
File.RESOURCE_ICON_PATH = os.path.join(os.path.dirname(__file__), 'static', 'img', 'mime')
File.RESOURCE_ICON_SIZES = ['16x16', '32x32']
File.RESOURCE_DEFAULT_ICON_SIZE = '32x32'

File.RESOURCE_EXT_MAPPINGS = {
        'docx': 'doc',
        'ppsx': 'pps',
        'ppt':  'pps',
        'pptx': 'pps',
        'xlsx': 'xls',
        }

def get_resource_icon_url(self, icon_size="32x32"):
    if icon_size not in self.RESOURCE_ICON_SIZES:
        icon_size = self.RESOURCE_DEFAULT_ICON_SIZE
    ext = self.extension
    if ext in self.RESOURCE_EXT_MAPPINGS:
        ext = self.RESOURCE_EXT_MAPPINGS[ext]
    icon = self.ext_to_icon_path(ext, icon_size)
    if os.path.exists(icon):
        return self.ext_to_url(ext, icon_size)
    else:
        return self.ext_to_url('unknown', icon_size)

File.get_resource_icon_url = get_resource_icon_url

def get_resource_icon_url_32(self):
    return self.get_resource_icon_url("32x32")

File.get_resource_icon_url_32 = get_resource_icon_url_32

def get_resource_icon_url_16(self):
    return self.get_resource_icon_url("16x16")

File.get_resource_icon_url_16 = get_resource_icon_url_16

def ext_to_icon_path(self, ext, icon_size):
    if not ext:
        ext = 'unknown'
    return os.path.join(self.RESOURCE_ICON_PATH, icon_size, 'file_extension_%s.png' % ext)

File.ext_to_icon_path = ext_to_icon_path

def ext_to_url(self, ext, icon_size):
    if not ext:
        ext = 'unknown'
    return '/'.join([self.RESOURCE_URL_BASE, icon_size, 'file_extension_%s.png' % ext])

File.ext_to_url = ext_to_url
