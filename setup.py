from setuptools import setup, find_packages

# read requirements/dependencies
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# read description/README.md
with open("README.md", 'r') as fh:
    long_description = fh.read()


setup(name='seep_hpo',
      version='0.0.1.dev0',
      packages=find_packages(),
      install_requires=requirements,

      package_data={'': ['test_data/*']},
      long_description=long_description,
      long_description_content_type='text/markdown',

      author='OMOP 2 Phenopacket development team',
      author_email='peter.robinson@jax.com',
      url='https://github.com/TheJacksonLaboratory/SeepHPO',
      description='Python version of LOINC2HPO',
      license='GPLv3',
      keywords='python loinc hpo',

      entry_points={'console_scripts': [
          'seep-hpo = seep_hpo.main:main'
      ]})
