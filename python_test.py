import os
import re
import sublime
import sublime_plugin


DEFAULT_TEST_COMMAND = "nosetests "
TEST_DELIMETER = ":"


class RunPythonTestCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.load_settings()
        self.clean_settings()
        command = self.prepare_command()
        self.view.window().run_command(
            "exec",
            {
                "cmd": [command],
                "shell": True,
                "working_dir": self.test_root,
            }
        )
        self.save_test_run(command)

    def load_settings(self):
        settings = (
            self.view.window().active_view()
            .settings().get("python_test_runner")
        )
        self.test_root = settings.get(
            'test_root', self.view.window().folders()[0]
        )
        self.test_command = settings.get('test_command', DEFAULT_TEST_COMMAND)
        self.before_test = settings.get('before_test')
        self.after_test = settings.get('after_test')
        self.test_delimeter = settings.get('test_delimeter', TEST_DELIMETER)
        
    def clean_settings(self):
        if 'nosetests' in self.test_command:
            if not self.test_command.endswith(' '): 
                self.test_command += ' ' 

    def get_test_path(self):
        abs_file = self.view.file_name()
        rel_path = os.path.relpath(abs_file, self.test_root)
        self.test_path = rel_path.replace('/', '.')
        return self.test_path[:-3]  # remove .py

    def prepare_command(self):
        command = self.test_command + self.get_test_path()
        if self.before_test:
            command = self.before_test + " ; " + command
        if self.after_test:
            command = command + " ; " + self.after_test
        return command

    def save_test_run(self, command):
        s = sublime.load_settings("PythonTestRunner.last-run")
        s.set("last_test_run", command)
        sublime.save_settings("PythonTestRunner.last-run")


class RunPythonSeparateTestCommand(RunPythonTestCommand):

    def get_test_path(self):
        test_path = super(RunPythonSeparateTestCommand, self).get_test_path()
        region = self.view.sel()[0]
        line_region = self.view.line(region)
        text_string = self.view.substr(
            sublime.Region(region.begin() - 8000, line_region.end())
        )
        test_name = TestMethodMatcher().find_test_path(
            text_string, delimeter=self.test_delimeter
        )
        if test_name:
            return test_path + test_name


class RunLastPythonTestCommand(RunPythonTestCommand):

    def prepare_command(self):
        s = sublime.load_settings("PythonTestRunner.last-run")
        return s.get("last_test_run")


class TestMethodMatcher(object):

    def find_test_path(self, test_file_content, delimeter=TEST_DELIMETER):
        test_method = self.find_test_method(test_file_content)
        if test_method:
            test_class = self.find_test_class(test_file_content)
            return delimeter + test_class + "." + test_method

    def find_test_method(self, test_file_content):
        match_methods = re.findall(r'\s?def\s+(test_\w+)\s?\(', test_file_content)
        if match_methods:
            return match_methods[-1]

    def find_test_class(self, test_file_content):
        match_classes = re.findall(r'\s?class\s+(\w+)\s?\(', test_file_content)
        if match_classes:
            try:
                return [c for c in match_classes if "Test" in c or "test" in c][-1]
            except IndexError:
                return match_classes[-1]
