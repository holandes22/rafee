import os
import errno
from os.path import join, exists, getmtime

from bs4 import BeautifulSoup
from jinja2 import Environment, BaseLoader
from jinja2.exceptions import TemplateNotFound


class FileSystemLoader(BaseLoader):

    def __init__(self, root_folder):
        self.root_folder = root_folder
        self.clean_tags = ['script', 'link', 'style']

    def clean_source(self, file):
        soup = BeautifulSoup(file.read())
        for tag in self.clean_tags:
            for item in soup.find_all(tag):
                item.extract()
        return soup.encode_contents()

    def get_source(self, environment, template):
        path = join(self.root_folder, template)
        if not exists(path):
            raise TemplateNotFound(template)
        mtime = getmtime(path)
        with open(path, 'rb') as f:
            source = self.clean_source(f).decode('utf-8')
        return source, path, lambda: mtime == getmtime(path)

    def list_templates(self):
        templates = []
        # list repos under root folder
        for repo in os.listdir(self.root_folder):  # repos under root
            repo_path = join(self.root_folder, repo)
            if os.path.isdir(repo_path):
                # list template folders under repos folders
                for template in os.listdir(repo_path):
                    template_path = join(repo_path, template)
                    if os.path.isdir(template_path):
                        if 'template.j2' in os.listdir(template_path):
                            name = join(repo, template, 'template.j2')
                            templates.append(name)
        return templates


class TemplateManager(object):

    def __init__(self, root_folder):
        self.root_folder = root_folder
        self.loader = FileSystemLoader(self.root_folder)
        self.env = Environment(loader=self.loader)
        self.template_names = self.loader.list_templates()

    def template_exists(self, template_name):
        if not template_name.endswith('template.j2'):
            template_name = join(template_name, 'template.j2')
        return template_name in self.template_names

    def get_template_info(self, template_name):
        name = template_name.replace('/template.j2', '')
        path = join(self.root_folder, name, 'data_source_url')
        value = None
        try:
            with open(path, 'rb') as f:
                line = f.readline()
                if line != '':
                    value = line.strip()
        except IOError as e:
            if e.errno != errno.ENOENT:
                raise
        # ID here is meaningless, but we need it to
        # satisfy the response expected by ember-data
        return {'id': 1, 'name': name, 'data_source_url': value}

    def get_templates_info(self):
        info = []
        for template_name in self.template_names:
            info.append(self.get_template_info(template_name))
        return info

    def render_from_string(self, template_str, **kwargs):
        template = self.env.from_string(template_str)
        return template.render(**kwargs)

    def render(self, template_name, **kwargs):
        template = self.env.get_template(
            join(template_name, 'template.j2'),
        )
        return template.render(**kwargs)
