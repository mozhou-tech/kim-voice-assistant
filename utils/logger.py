import logging
import src.config as config_path
import os


def init(args):

    logging.basicConfig(
        filename=os.path.join(
            config_path.LOG_PATH, "xiaoyun.log"
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

