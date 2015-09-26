from setuptools import setup

setup(
    name='equibel',
    version='0.9.1a1', # v0.9.1 alpha build
    
    description='A toolkit for equivalence-based belief change',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    keywords=['AI', 'belief change', 'belief merging', 'agent network'],

    url='https://github.com/asteroidhouse/equibel',
    author='Paul Vicol',
    author_email='pvicol@sfu.ca',
    license='MIT',

    packages=[
        'equibel',
        'equibel.simbool',
        'equibel.parsers',
        'equibel.formatters',
    ],

    include_package_data = True,

    install_requires=[
        'networkx',
        'ply',
        'colorama',
    ],

    entry_points='''
        [console_scripts]
        equibeli=equibel.equibeli:cli
    ''',
)
