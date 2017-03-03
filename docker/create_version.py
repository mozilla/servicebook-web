import json
import os
import subprocess
import sys

sys.path.append('..')
from serviceweb import __version__


HERE = os.path.dirname(__file__)


with open(os.path.join(HERE, '..', 'serviceweb', 'templates',
          'version.json')) as f:
    version = json.loads(f.read())

commit = subprocess.check_output(["git", "describe", "--always"])
commit = str(commit.strip(), 'utf8')

version['commit'] = commit
version['version'] = __version__

print(json.dumps(version))
