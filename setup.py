import re
from distutils.core import setup

requirements = [
	'websockets',
	'flask'
]

def get_version():
    with open('blueberry/__main__.py') as inf:
      match = re.search(r"((\d\.){2,5}\d)", inf.read(), re.MULTILINE)

      if match is None:
          raise RuntimeError('Version could not be found.')
    return match.groups()[0]

setup(
    name='blueberry',
    version=get_version(),
    description='Decentralised virtual network application.',
    install_requires=requirements,
)
