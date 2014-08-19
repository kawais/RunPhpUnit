import os, sublime_plugin, sublime, subprocess, re
from os.path import expanduser

report = []

# show console
# sublime.active_window().run_command("show_panel", {"panel": "console", "toggle": True})

def debug_message(msg):
    print("[Run Phpunit] " + str(msg))

def runcmd(cmd):
    global report
    data = None

    if st_version != 3:
        for index, arg in enumerate(cmd[:]):
            cmd[index] = arg.encode(sys.getfilesystemencoding())


    debug_message(' '.join(cmd))

    info = None
    if os.name == 'nt':
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = subprocess.SW_HIDE

    home = expanduser("~")

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=info, cwd=home)


    if proc.stdout:
        data = proc.communicate()[0]

    if st_version == 3:
        result = data.decode()
    else:
        result = data

    print(result)
    pattern = re.compile('\S+:\d+')
    match = pattern.findall(result)
    lines = result.split("\n")
    msg_list = []
    msg_list.append(lines[-2])
    if match:
        msg_list=msg_list+match
        report=match
    return msg_list
    # return result




class Pref:
    def load(self):
        self.settings = sublime.load_settings('runphpunit.sublime-settings')
    def get_setting(self, key):
        return self.settings.get(key)

pref = Pref()
pref.load()

st_version = 2
if sublime.version() == '' or int(sublime.version()) > 3000:
    st_version = 3

class RunAllTestsCommand(sublime_plugin.TextCommand):
    def run(self, edit, paths):
        cmd = []
        cmd.append(pref.get_setting('phpunit_path'))
        if pref.get_setting('phpunit_args'):
            cmd.append(pref.get_setting('phpunit_args'))
        cmd.append(paths.pop())
        msg = runcmd(cmd)
        self.show_quick_panel(msg)
    def show_quick_panel(self,msg):
        self.view.window().show_quick_panel(msg,self.on_quick_panel_done)
    def on_quick_panel_done(self,picked):
        global report
        if report[picked-1]:
            self.view.window().open_file(report[picked-1],sublime.ENCODED_POSITION)

class ShowLastResultCommand(sublime_plugin.TextCommand):
    def run(self,edit):
        global report
        self.view.window().show_quick_panel(report,self.on_quick_panel_done)
    def on_quick_panel_done(self,picked):
        global report
        if report[picked]:
            self.view.window().open_file(report[picked],sublime.ENCODED_POSITION)



class RunThisTestsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_name=self.view.file_name()
        # path=file_name.split("\\")
        # current_driver=path[0]
        # path.pop()
        # current_directory="\\".join(path)
        cmd = []
        cmd.append(pref.get_setting('phpunit_path'))
        if pref.get_setting('phpunit_args'):
            cmd.append(pref.get_setting('phpunit_args'))
        cmd.append(file_name)
        msg = runcmd(cmd)
        self.show_quick_panel(msg)
    def show_quick_panel(self,msg):
        self.view.window().show_quick_panel(msg,self.on_quick_panel_done)
    def on_quick_panel_done(self,picked):
        global report
        if report[picked-1]:
            self.view.window().open_file(report[picked-1],sublime.ENCODED_POSITION)
        return


class CmdHereCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_name=self.view.file_name()
        path=file_name.split("\\")
        current_driver=path[0]
        path.pop()
        current_directory="\\".join(path)
        command= "cd "+current_directory+" & "+current_driver+" & start cmd"
        os.system(command)