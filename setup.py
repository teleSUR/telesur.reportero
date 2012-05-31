from setuptools import setup, find_packages
import os

version = '1.0'
long_description = open("README.rst").read() + "\n" + \
                   open(os.path.join("docs", "CREDITS.txt")).read() + "\n" + \
                   open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='telesur.reportero',
      version=version,
      description="",
      long_description=long_description,
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Topic :: Office/Business :: News/Diary",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='telesur reportero',
      author='Franco Pellegrini',
      author_email='frapell@ravvit.net',
      url='https://github.com/teleSUR/telesur.reportero',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['telesur'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'borg.localrole',
        'plone.app.dexterity>=1.2.1',
        'plone.formwidget.captcha',
        'plone.namedfile[blobs]',
        'collective.prettydate',
        'httplib2',
        ],
      extras_require={
        'test': ['plone.app.testing'],
        },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
