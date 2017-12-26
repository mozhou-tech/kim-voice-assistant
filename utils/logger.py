import logging
import os
from config.path import LOG_PATH


def init(args):

    logging.basicConfig(
        filename=os.path.join(
            LOG_PATH, "xiaoyun.log"
        ),
        filemode="w",
        format='%(asctime)s %(filename)s[line:%(lineno)d] \
        %(levelname)s %(message)s',
        level=logging.INFO)
    logger = logging.getLogger()

    logger.getChild("src.stt").setLevel(logging.INFO)
    if args.debug:
        logger.setLevel(logging.DEBUG)
    elif args.info:
        logger.setLevel(logging.INFO)
    return logger



