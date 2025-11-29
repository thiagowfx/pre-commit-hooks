from setuptools import setup

setup(
    name='pre_commit_hooks',
    version='0.0.0',
    install_requires=['PyYAML==6.0.3'],
    scripts=['scripts/if_this_then_that.py'],
)
