import os
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
        with file(path) as f:
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
        self.template_pattern = 'template.j2'
        self.loader = FileSystemLoader(self.root_folder)
        self.env = Environment(loader=self.loader)
        self.template_names = self.loader.list_templates()

    @classmethod
    def render_template(cls, template, **kwargs):
        return template.render(**kwargs)

    def render(self, repo_name, template_name, **kwargs):
        template = self.env.get_template(
            join(repo_name, template_name, 'template.j2'),
        )
        return self.render_template(template, **kwargs)
