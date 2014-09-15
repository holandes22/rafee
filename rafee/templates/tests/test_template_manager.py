import os
import unittest
from mock import patch, MagicMock
from nose.tools import nottest

from rafee.templates.manager import TemplateManager

TEMPLATE = 'Hello!'
TEMPLATE_WITH_VALUES = 'Hello {{ name }}!'
TEMPLATE_WITH_INVALID_TAGS = '''
<html>
    <head>
        <script>content</script>
        <style>content</style>
        <link>content</link>
    </head>
    </body>
        <p>Hi <span>world</span></p>
        <script>console.log('hey')</script>
    </body>
</html>
'''


class TemplateManagerTests(unittest.TestCase):

    def setUp(self):
        self.folder_structure = {
            'repo1': ['dir1', 'template.j2'],
            'repo2': ['template.j2'],
            'invalid': ['subdir1', 'file.ext'],
        }
        #self.os_patcher = patch('rafee.templates.manager.os')
        #self.os_mock = self.os_patcher.start()
        #self.os_mock.listdir.side_effect = self.listdir_side_effect
        #self.folder = '/fake/templates'
        #self.manager = TemplateManager(self.folder)

    def tearDown(self):
        return
        self.os_patcher.stop()

    @nottest
    def listdir_side_effect(self, path):
        if path == self.folder:
            return self.folder_structure.keys()
        name = os.path.basename(path)
        return self.folder_structure[name]

    @nottest
    def test_list(self):
        # expected = [n for n in self.folder_structure.keys() if 'repo' in n]
        # self.assertEqual(expected, self.manager.template_names)
        pass

    @nottest
    def test_list_returns_only_folders_from_top_level(self):
        # /templates/repo/template1/template.j2 - OK
        # /templates/repo/nesteddir/template1/template.j2 - NOT OK
        # TODO: Not sure how to test this
        pass

    @nottest
    def test_get_source(self):
        #with patch('rafee.templates.manager.open', create=True) as open_mock:
        #    open_mock.return_value = MagicMock(spec=file)
        #    file_handle = open_mock.return_value.__enter__.return_value
        #    file_handle.read.return_value = TEMPLATE
        #    self.manager.render()
        pass

    @nottest
    def test_render(self):
        pass

    @nottest
    def test_render_template(self):
        pass

    @nottest
    def test_clean_source(self):
        pass
