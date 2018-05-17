from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='banner-snatcher',
      version='1.0',
      description='Program for retrieving banners on open ports',
      long_description=readme(),
      url='https://github.com/heywoodlh/banner-snatcher',
      author='Spencer Heywood',
      author_email='l.spencer.heywood@protonmail.com',
      license='MIT',
      packages=['banner-snatcher'],
      scripts=['bin/bansnatch'],
      install_requires=[
          'dnspython',
          'netaddr'
      ],
zip_safe=False)
