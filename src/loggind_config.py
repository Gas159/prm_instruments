import logging


# ANSI escape codes
class ColoredFormatter(logging.Formatter):
    COLOR_RESET = "\033[0m"
    COLOR_INFO = "\033[92m"  # Зеленый
    COLOR_DEBUG = "\033[93m"  # Желтый

    def format(self, record):
        if record.levelno == logging.INFO:
            record.msg = f"{self.COLOR_INFO}{record.msg}{self.COLOR_RESET}"
        elif record.levelno == logging.DEBUG:
            record.msg = f"{self.COLOR_DEBUG}{record.msg}{self.COLOR_RESET}"
        return super().format(record)


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Создание обработчика для вывода в терминал
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Настройка форматирования с цветами
    formatter = ColoredFormatter(
        "%(asctime)s - %(levelname)s - [%(name)s] - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    # Добавление обработчика к логгеру
    logger.addHandler(console_handler)
