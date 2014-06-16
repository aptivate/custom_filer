from django.conf.urls.defaults import patterns, url

from views import ZipFolderView

urlpatterns = patterns('',
    url(r'folder/(?P<pk>\d+)/$',
        ZipFolderView.as_view(),
        name='custom_filer_zip_folder'),
    )