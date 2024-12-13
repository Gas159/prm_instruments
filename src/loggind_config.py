import logging
import textwrap


class ColoredFormatter(logging.Formatter):
    # Цветовые коды
    COLOR_RESET = "\033[0m"
    COLOR_INFO = "\033[92m"  # Зеленый
    COLOR_DEBUG = "\033[93m"  # Желтый
    COLOR_WARNING = "\033[94m"  # Синий
    COLOR_ERROR = "\033[95m"  # Фиолетовый
    COLOR_CRITICAL = "\033[38;5;202m"  # Красный

    # Настройка максимальной ширины строки для переносов
    WRAP_WIDTH = 80
    WRAP_INDENT = "    "  # Отступ для переноса

    def format(self, record):
        # Добавление цвета для каждого уровня
        if record.levelno == logging.INFO:
            record.msg = f"{self.COLOR_INFO}{record.msg}{self.COLOR_RESET}"
        elif record.levelno == logging.DEBUG:
            record.msg = f"{self.COLOR_DEBUG}{record.msg}{self.COLOR_RESET}"
        elif record.levelno == logging.WARNING:
            record.msg = f"{self.COLOR_WARNING}{record.msg}{self.COLOR_RESET}"
        elif record.levelno == logging.ERROR:
            record.msg = f"{self.COLOR_ERROR}{record.msg}{self.COLOR_RESET}"
        elif record.levelno == logging.CRITICAL:
            record.msg = f"{self.COLOR_CRITICAL}{record.msg}{self.COLOR_RESET}"

        # Перенос длинных строк
        record.msg = textwrap.fill(record.msg, width=self.WRAP_WIDTH, subsequent_indent=self.WRAP_INDENT)

        # Форматирование базового сообщения
        return super().format(record)


def setup_logging():
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.DEBUG)

    # Создание обработчика для вывода в терминал
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Настройка форматирования с цветами и переносами
    formatter = ColoredFormatter(
        "%(asctime)s - %(levelname)s - [%(name)s] - %(filename)s:%(lineno)d -  \n %(funcName)s() - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # formatter = ColoredFormatter(
    #     "%(filename)s:%(lineno)d - %(funcName)s() -\n %(message)s",
    #     datefmt="%Y-%m-%d %H:%M:%S",
    # )
    console_handler.setFormatter(formatter)

    # Добавление обработчика к логгеру
    logger.addHandler(console_handler)
