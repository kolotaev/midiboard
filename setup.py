from os import path
from setuptools import setup, find_packages


info = {}
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'midiboard', 'info.py'), mode='r') as f:
    exec(f.read(), info)


if __name__ == '__main__':
    setup(
        name=info['NAME'],
        description='',
        # keywords='',
        version=info['VERSION'],
        author='',
        author_email='',
        license='MIT',
        url='',
        long_description='',
        # entry_points={
        #     'console_scripts': [
        #         '%s = compose.main:execute' % info['NAME'],
        #     ],
        # },
        # py_modules=['main'],
        python_requires='>=3',
        install_requires=[
            'pynput~=1.7',
            'mido~=1.2',
            'python-rtmidi',
            'PyQt5~=5.15',
        ],
        extras_require={
            'dev': [
                'pytest>=4.6',
            ],
        },
        packages=find_packages(exclude='tests'),
        classifiers=[
            'Natural Language :: English',
            'License :: OSI Approved :: MIT',
            'Programming Language :: Python',
            # 'Programming Language :: Python :: 2',
            # 'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: Implementation :: CPython',
        ],
    )
