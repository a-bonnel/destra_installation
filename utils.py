def colorize(text, color):
    class Color:
        RESET = "\033[0m"
        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"
        RED = "\033[91m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        MAGENTA = "\033[95m"
        CYAN = "\033[96m"

    colors = {
        "reset": Color.RESET,
        "bold": Color.BOLD,
        "underline": Color.UNDERLINE,
        "red": Color.RED,
        "green": Color.GREEN,
        "yellow": Color.YELLOW,
        "blue": Color.BLUE,
        "magenta": Color.MAGENTA,
        "cyan": Color.CYAN,
    }

    return f"{colors.get(color.lower(), '')}{text}{Color.RESET}"
