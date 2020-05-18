import logging
import sys

DEFAULT_LOG_FMT = '%(asctime)s %(name)-20s %(levelname)-3s : %(message)s'
logging.basicConfig(level=logging.INFO, format=DEFAULT_LOG_FMT)


def main():
    """Python version of LOINC2HPO"""
    logger = logging.getLogger('seep_hpo')
    logger.info("I'm done!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
