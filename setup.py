from setuptools import setup, find_packages
import pathlib
import styling
import constants

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='redcoffee',
    version='0.6', 
    description='A command-line tool to generate PDF for SonarQube Reports',
    long_description=README,
    long_description_content_type='text/markdown',
      # Change this if your README is not markdown
    packages=find_packages(),  # Automatically find packages
    py_modules=['redcoffee', 'styling', 'constants'],
    install_requires=[
        'click',
        'reportlab',
        'pytest'
    ],
    entry_points='''
        [console_scripts]
        redcoffee=redcoffee:cli
    ''',
    include_package_data=True,
)