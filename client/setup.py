from setuptools import setup, find_packages

requirements  = [require.strip() for require in open('requirements.txt', 'r').readlines()]

setup(
    name='dragon_bear_classifer_client',
    version='0.1',
    author = "Anna Dixon",
    author_email = "anna@datafoss.com",
    scripts = ['classifier_client/dragon_bear_classifier_client_main.py'],
    packages = find_packages('classifier_client'),
    package_dir = {'classifier_client' : 'classifier_client'},
    package_data = {'classifier_client' : ['data_sample/*']},
    install_requires=requirements,
    entry_points={"console_scripts": ["dragon_bear_client=classifier_client.dragon_bear_classifier_client_main:cli"]},
)