from setuptools import setup, find_packages

# read requirements/dependencies
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# read description/README.md
with open("README.md", 'r') as fh:
    long_description = fh.read()


setup(name='loinchpo',
      version='1.1.2.dev',
      packages=find_packages(),
      install_requires=requirements,
      package_data={'':  ['test/*']},
      data_files=[('', ['requirements.txt', 'LICENSE.txt'])],
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Michael Gargano',
      author_email='michael.gargano@jax.com',
      url='https://github.com/TheJacksonLaboratory/loinchpo',
      description='Python version of LOINC2HPO',
      license='GPLv3',
      keywords='python, loinc, hpo, clinical, omop, human phenotype ontology',
      entry_points={'console_scripts': [
          'loinchpo = loinchpo.main:cli'
      ]})
