import subprocess

text = """first
second
third"""

proc = subprocess.Popen(['telegram-cli',
                         '--log-level', '0',
                         '--verbosity', '0',
                         '--wait-dialog-list',
                         '--disable-link-preview',
                         '--disable-colors',
                         '--disable-readline',
                         '--exec', 'msg Jalp "{}"'.format(text.replace('\n', '\\n'))])
