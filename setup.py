try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def version():
    with open('dockermon.py') as fo:
        for line in fo:
            if '__version__' not in line:
                continue
            # "__version__ = '0.1.0'" -> "0.1.0"
            return line.split('=')[1].strip().replace("'", '')


def readme():
    with open('README.md') as fo:
        return fo.read()

setup(
    name='dockermon',
    version=version(),
    description='docker monitor using docker /events HTTP streaming API',
    long_description=readme(),
    author='CyberInt',
    author_email='tools@cyberint.com',
    license='MIT',
    url='https://github.com/CyberInt/dockermon',
    py_modules=['dockermon'],
    tests_require=['nose', 'flake8', 'tox'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
