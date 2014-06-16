from django.views.generic import View
from django.http import HttpResponse
from filer.models import Folder
from django.shortcuts import get_object_or_404

import zipfile
import os
from StringIO import StringIO

class ZipFolderView(View):

    def zipfiles(self, zip, files, level):
        for f in files:
            hierarchy = [x.name for x in f.logical_path[level:]]
            hierarchy.append(f.original_filename)
            filename = os.path.join(*hierarchy)
            zip.writestr(filename, f.file.read())

    #recursively zip up folders
    def zipfolder(self, zip, folder, level):
        if folder.files:
            self.zipfiles(zip, folder.files, level)
        for child_folder in folder.get_children():
            self.zipfolder(zip, child_folder, level)

    #get the target folder from the given id and zip it up
    #consider putting in permissions check.
    #consider adding DEPTH to recursion.
    def get(self, request, pk):
        object = get_object_or_404(Folder, pk=pk)
        buffer = StringIO()
        zip = zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED)
        self.zipfolder(zip, object, object.level)
        zip.close()
        buffer.flush()
        ret_zip = buffer.getvalue()
        buffer.close()
        filename = "%s.zip" % object.name.replace(' ','_')
        response = HttpResponse(mimetype='application/zip')
        response['Content-Disposition'] = 'attachment ; filename=%s' % filename
        response.write(ret_zip)
        return response
