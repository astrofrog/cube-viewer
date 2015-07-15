import os
from setuptools import setup, Command

entry_points = """
[glue.plugins]
cube_viewer = cube_viewer.glue_plugin:setup
"""

setup(name='cube-viewer',
      version='0.0.dev',
      url='http://www.github.com/astrofrog/cube-viewer.git',
      description='Simple 3D FITS cube viewer',
      author='Thomas Robitaille',
      author_email='thomas.robitaille@gmail.com',
      packages=['cube_viewer'],
      package_data={'cube_viewer':['*.ui']},
      keywords=['Scientific/Engineering'],
      classifiers=[
                   "Development Status :: 4 - Beta",
                   "Programming Language :: Python",
                   "License :: OSI Approved :: BSD License",
                  ],
      scripts=[os.path.join('scripts', 'cube-viewer')],
      entry_points=entry_points
     )