from setuptools import setup, find_packages


if __name__ == '__main__':
    setup(
        name='midiboard',
        description='',
        # keywords='',
        version='0.1',
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
            'PyQt5~=6.5',
        ],
        extras_require={
            'dev': [
                'pytest>=4.6',
                # 'pyinstaller==5.5'
            ],
        },
        # packages=['midiboard'],
        include_package_data=True,
        packages=find_packages(exclude='tests'),
        classifiers=[
            'Natural Language :: English',
            'License :: OSI Approved :: MIT',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: Implementation :: CPython',
        ],
    )
