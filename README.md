# Exoticus Discord Bot

## Description
**Exoticus** is an open-source Discord bot that utilizes [Hikari](https://docs.hikari-py.dev/en/latest/) and [Hikari-Lightbulb](https://hikari-lightbulb.readthedocs.io/en/latest/getting-started.html) as libraries, providing an alternative to discord.py. The bot is currently exclusively operational within my Discord server (and I would like to keep it that way). **Exoticus** is designed to serve as an educational example, showcasing the effective application of Hikari, and as a source of inspiration for diverse project ideas. Whether it's implementing a leveling system or a ticket system, this bot offers valuable insights, especially for those who are new to the library.

---

## Features

- **Filter Extension:**
  - The Filter Extension moderates content by automatically handling Discord invites, blocking NSFW links, and managing LFG (Looking For Group) keywords.
- **Functions Extension:**
  - The Functions Extension is a collection of fundamental utility functions designed to enhance error handling and simplify common tasks when working with the Hikari library.
  - ***If you're new to Hikari**, I recommend checking out this extension as it provides essential code snippets for common tasks.*
- **Join Extension:**
  - The Join Extension manages join and leave events, assigns join roles, updates and inserts members in a database, and logs joins and leaves in a simple yet efficient way. It also renders and sends out personalized [join cards](https://i.imgur.com/2AeUrOT.png).
- **Level Extension:**
  - The Level Extension automates XP tracking, leveling, and role assignment. Users gain XP through messages and voice chat. The extension provides commands to check ranks, give or take XP and it provieds a leaderboard. Additionally, it sends level-up messages and assigns roles based on XP levels.
- **Tickets Extension:**
  - The Ticket Extension offers essential Discord bot features, along with unique capabilities like assigning team IDs to members. It includes an anonymous feedback system where users can rate moderators with 1-5 stars. The average ratings are displayed in an embed for team members or everyone as preferred.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/IQExotic/Exoticus.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Edit the file named `.env` in the root directory and replace "YOUR_BOT_TOKEN_HERE" with your bot token:

   ```
   token=YOUR_BOT_TOKEN_HERE
   ```

4. Run the bot:

   ```bash
   python bot.py
   ```
   On Linux or Mac, it might be:
   ```bash
   python3 bot.py
   ```

## Usage

Please avoid direct copying and pasting of the code. Instead, treat it as a valuable learning resource or a wellspring of inspiration. If you plan to integrate the entire bot into your project or duplicate complete extensions, kindly seek permission beforehand.

In instances of uncertainty regarding usage or appropriateness, it is strongly recommended to communicate with me directly. Feel free to reach out, and we can collaborate to find an appropriate solution. (Note: My Discord DMs are usually quite full, so I recommend joining my [Discord server](https://discord.gg/7kqsMgNURY) and opening a ticket.)

## Contributing

If you would like to contribute to the development of the bot, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and submit a pull request.


## Examples
- Join Card

  ![](https://i.imgur.com/2AeUrOT.png)

- Leaderboard

  
  ![](https://i.imgur.com/cb7IMHk.png)


