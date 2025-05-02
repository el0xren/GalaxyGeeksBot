from logging import basicConfig, debug, info, error, warning, INFO, FileHandler, StreamHandler

basicConfig(format='[%(asctime)s] [%(filename)s:%(lineno)s %(levelname)s] %(funcName)s: %(message)s',
                    handlers=[FileHandler('log.txt'), StreamHandler()],
                    level=INFO)

LOGD = debug
LOGI = info
LOGE = error
LOGW = warning
