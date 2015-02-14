import os
import errno
from base64 import urlsafe_b64encode

import pytest
from mock import patch, Mock, MagicMock
from jinja2.exceptions import TemplateNotFound

from rafee.test_utils.assert_helpers import assert_items_equal
from rafee.templates.manager import FileSystemLoader, TemplateManager


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


class TestFileSystemLoader(object):

    folder_structure = {
        'repo1': {'t1': ['template.j2'], 't2': ['invalid.j2']},
        'repo2': {'t1': ['template.j2', 'dir'], 't2': ['template.j2']},
        'repo3': {'t1': ['subdir1', 'file.ext']},
    }
    root_folder = '/fake/templates'

    @classmethod
    def setup_class(cls):
        cls.os_patcher = patch('rafee.templates.manager.os')
        os_mock = cls.os_patcher.start()
        os_mock.listdir.side_effect = cls.listdir_side_effect

    @classmethod
    def teardown_class(cls):
        cls.os_patcher.stop()

    @classmethod
    def listdir_side_effect(cls, path):
        if path == cls.root_folder:
            return cls.folder_structure.keys()
        name = os.path.basename(path)
        if name in cls.folder_structure:
            return cls.folder_structure[name].keys()
        repo = os.path.basename(os.path.dirname(path))
        return cls.folder_structure[repo][name]

    def clean_string(self, s):
        return s.replace(' ', '').replace('\n', '')

    def test_list(self):
        expected = [
            os.path.join('repo1', 't1', 'template.j2'),
            os.path.join('repo2', 't1', 'template.j2'),
            os.path.join('repo2', 't2', 'template.j2'),
        ]
        loader = FileSystemLoader(self.root_folder)
        assert_items_equal(expected, loader.list_templates())

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
        assert expected_path == path
        expected_source = '''
        <html>
            <head>
            </head>
            <body>
                <p>Hi <span>world</span></p>
            </body>
        </html>
        '''
        assert self.clean_string(expected_source) == self.clean_string(source)

    def test_get_source_raises_error_if_no_template(self):
        loader = FileSystemLoader(self.root_folder)
        with pytest.raises(TemplateNotFound):
            loader.get_source(Mock(), 't')


@patch('rafee.templates.manager.FileSystemLoader')
@patch('rafee.templates.manager.open', create=True)
def test_get_templates_info(open_m, FileSystemLoader_m):
    loader = FileSystemLoader_m.return_value
    loader.list_templates.return_value = [
        'r1/t/template.j2',
        'r2/t/template.j2',
        'r3/t/template.j2',
    ]

    open_m.return_value = MagicMock(spec=file)
    file_handle = open_m.return_value.__enter__.return_value
    error = IOError()
    error.errno = errno.ENOENT
    file_handle.readline.side_effect = ['http://b.c/r', '', error]

    manager = TemplateManager('/fake')
    templates_info = manager.get_templates_info()
    enc = urlsafe_b64encode
    expected = [
        {'id': enc('r1/t'), 'name': 'r1/t', 'data_source_url': 'http://b.c/r'},
        {'id': enc('r2/t'), 'name': 'r2/t', 'data_source_url': None},
        {'id': enc('r3/t'), 'name': 'r3/t', 'data_source_url': None},
    ]
    # last call
    open_m.assert_called_with('/fake/r3/t/data_source_url', 'rb')
    assert_items_equal(expected, templates_info)


@patch('rafee.templates.manager.FileSystemLoader')
@patch('rafee.templates.manager.Environment')
def test_template_exists(Environment_m, FileSystemLoader_m):
    loader = FileSystemLoader_m.return_value
    loader.list_templates.return_value = [
        'c/t1/template.j2', 'c/t2/template.j2'
    ]
    manager = TemplateManager('/fake')
    assert manager.template_exists('c/t1')
    assert manager.template_exists('c/t1/template.j2')
    assert not manager.template_exists('none')
