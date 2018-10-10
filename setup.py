from setuptools import setup, find_packages
from ezretry import __version__

setup(
    name="ezretry",
    packages=find_packages(),
    version=__version__,
    description="Not only simply retry, it will call a function for user define Exceptions before retry",
    author="kailyn",
    author_email='1074741118@qq.com',
    url="https://github.com/cnkailyn/ezretry",
    keywords=['retry', 'ezretry'],
    classifiers=[],
    entry_points={
        'console_scripts': []
    },
    install_requires=[]
)
