from setuptools import setup

setup(
    name='equibel',
    version='0.9.3a1', # v0.9.3 alpha build
    
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

    keywords=['AI', 'belief change', 'belief revision', 'belief merging', 'multi-agent network'],

    url='https://github.com/asteroidhouse/equibel',
    author='Paul Vicol',
    author_email='pvicol@sfu.ca',
    license='MIT',

    packages=[
        'equibel',
    ],

    include_package_data = True,

    install_requires=[
        'networkx',
        'ply',
        'sympy',
    ],
)
