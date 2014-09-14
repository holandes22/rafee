import os
from os.path import join


class TemplateManager(object):

    def __init__(self, folder):
        self.folder = folder
        self.template_pattern = 'template.j2'

    def get_templates(self):
        templates = []
        for item in os.listdir(self.folder):
            full_path = join(self.folder, item)
            if os.path.isdir(full_path):
                content = os.listdir(full_path)
                if self.template_pattern in content:
                    templates.append(item)
        return templates

    def render(self):
        with open('somedir', 'r') as f:
            print f.read()
