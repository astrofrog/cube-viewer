import os
from setuptools import setup, Command


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
      scripts=[os.path.join('scripts', 'cube-viewer')]
     )