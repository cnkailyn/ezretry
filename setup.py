from setuptools import setup, find_packages

setup(
    name="ezretry",
    packages=find_packages(),
    version='0.0.1',
    description="Not only simply retry, it will call a function for user define Exceptions before retry",
    author="wangkailin",
    author_email='1074741118@qq.com',
    url="https://github.com/cnkailyn/ezretry",
    keywords=['retry', 'ezretry'],
    classifiers=[],
    entry_points={
        'console_scripts': []
    },
    install_requires=[]
)
