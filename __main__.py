from __future__ import annotations

from bot import Bot, __version__

def main():
    bot = Bot(__version__)
    bot.run()

if __name__ == "__main__":
    main()