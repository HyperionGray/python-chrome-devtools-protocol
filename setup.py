from pathlib import Path
from setuptools import setup, find_packages

here = Path(__file__).parent

with (here / 'README.md').open(encoding='utf8') as f:
    long_description = f.read()

setup(
    name='chrome-devtools-protocol',
    version='0.3.0',
    description='Python type wrappers for Chrome DevTools Protocol (CDP)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/HyperionGray/python-chrome-devtools-protocol',
    author='Mark E. Haase <mehaase@gmail.com>, Brian Mackintosh <bcmackintosh@gmail.com>',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.7',
    keywords='chrome devtools protocol cdp',
    package_data={'cdp': ['py.typed']},
    packages=find_packages(exclude=['build', 'docs', 'examples', 'generator']),
    install_requires=[
        'deprecated'
    ]
)
