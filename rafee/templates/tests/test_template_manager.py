import os
import unittest

from mock import patch, Mock, MagicMock
from nose.tools import nottest
from jinja2.exceptions import TemplateNotFound

from rafee.templates.manager import FileSystemLoader


TEMPLATE_WITH_INVALID_TAGS = '''
<html>
    <head>
        <script>content</script>
        <style>content</style>
        <link href='blah'/>
    </head>
    <body>
        <p>Hi <span>world</span></p>
        <script>console.log('hey')</script>
    </body>
</html>
'''


class FileSystemLoaderTests(unittest.TestCase):

    def setUp(self):
        self.folder_structure = {
            'repo1': {'t1': ['template.j2'], 't2': ['invalid.j2']},
            'repo2': {'t1': ['template.j2', 'dir'], 't2': ['template.j2']},
            'repo3': {'t1': ['subdir1', 'file.ext']},
        }
        self.os_patcher = patch('rafee.templates.manager.os')
        self.os_mock = self.os_patcher.start()
        self.os_mock.listdir.side_effect = self.listdir_side_effect
        self.root_folder = '/fake/templates'

    def tearDown(self):
        self.os_patcher.stop()

    @nottest
    def listdir_side_effect(self, path):
        if path == self.root_folder:
            return self.folder_structure.keys()
        name = os.path.basename(path)
        if name in self.folder_structure:
            return self.folder_structure[name].keys()
        repo = os.path.basename(os.path.dirname(path))
        return self.folder_structure[repo][name]

    def clean_string(self, s):
        return s.replace(' ', '').replace('\n', '')

    def test_list(self):
        expected = [
            os.path.join('repo1', 't1', 'template.j2'),
            os.path.join('repo2', 't1', 'template.j2'),
            os.path.join('repo2', 't2', 'template.j2'),
        ]
        loader = FileSystemLoader(self.root_folder)
        self.assertItemsEqual(expected, loader.list_templates())

    @patch('rafee.templates.manager.getmtime')
    @patch('rafee.templates.manager.open', create=True)
    @patch('rafee.templates.manager.exists')
    def test_get_source_removes_tags(self, exists_m, open_m, getmtime_m):
        exists_m.return_value = True
        open_m.return_value = MagicMock(spec=file)
        file_handle = open_m.return_value.__enter__.return_value
        file_handle.read.return_value = TEMPLATE_WITH_INVALID_TAGS
        loader = FileSystemLoader(self.root_folder)
        source, path, update = loader.get_source(Mock(), 't')
        expected_path = os.path.join(self.root_folder, 't')
        self.assertEqual(expected_path, path)
        expected_source = '''
        <html>
            <head>
            </head>
            <body>
                <p>Hi <span>world</span></p>
            </body>
        </html>
        '''
        self.assertEqual(
            self.clean_string(expected_source),
            self.clean_string(source),
        )

    def test_get_source_raises_error_if_no_template(self):
        loader = FileSystemLoader(self.root_folder)
        with self.assertRaises(TemplateNotFound):
            loader.get_source(Mock(), 't')
