from __future__ import annotations

from pathlib import Path

import hikari
import lightbulb
import datetime as dt

from bot.config import Config
from bot.database.db import Database

class Bot(lightbulb.BotApp):

    def __init__(self, version, config) -> None:
        self.dt = dt
        self.config = config
        self.version = version
        self._extensions = [p.stem for p in Path(".").glob("./bot/extensions/*.py")]
        self._dynamic = "./bot/data/dynamic"  # for error logs
        self._static = "./bot/data/static"
        self._transcripts = "./bot/data/transcripts"  # for ticket logs
        self.db = Database(self)

        if self.config.TOKEN:
            super().__init__(
                token=self.config.TOKEN,
                intents=hikari.Intents.ALL_UNPRIVILEGED
        | hikari.Intents.MESSAGE_CONTENT
        | hikari.Intents.GUILD_MEMBERS,
            )
        else:
            raise ValueError("No token provided")

    def run(self) -> None:
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)
        self.event_manager.subscribe(hikari.StoppedEvent, self.on_stopped)
        print("⭕ • Running bot...")

        super().run(
            activity=hikari.Activity(
                name=f"@Exoticus • Version {self.version}",
            ),
            status=hikari.Status.ONLINE
        )

    async def on_starting(self, event: hikari.StartingEvent) -> None:
        print("🔄 • Running setup...")

        print("🔄 • Connecting to database...")
        try:
            await self.db.connect()
            print("✅ • Connected to database.")
        except Exception as e:
            print(f"❌ • Failed to connect to database")
            print(e)
        

        for ext in self._extensions:
            try:
                self.load_extensions(f"bot.extensions.{ext}")
                print(f"☑️  • {ext} extension loaded")
            except Exception as e:
                print(f"❌ • {ext} extension failed to load")
                print(e)

        print("✅ • Setup complete.")

    async def on_started(self, event: hikari.StartedEvent) -> None:
        print("🔄 • Connecting to Discord...")
        try:
            heartbeat_latency = (self.heartbeat_latency * 1_000)
            print(f"✅ • Connected to Discord | {heartbeat_latency:,.0f} ms.")
        except Exception as e:
            print(f"❌ • Failed to connect to Discord")
            print(e)

        print("🔄 • Synchronising database...")
        try:
            await self.db.sync()
            print("✅ • Synchronised database.")
        except Exception as e:
            print(f"❌ • Failed to synchronise database")
            print(e)

        me = self.get_me()
        if me is not None:
            self.client_id = me.id

        print(f"✅ • Bot Ready! | Version {self.version}")

    async def on_stopping(self, event: hikari.StoppingEvent) -> None:
        print("🔄 • Shutting down...")
        print("🔄 • Closing connection to Discord...")

    async def on_stopped(self, event: hikari.StoppedEvent) -> None:
        print("🔄 • Closing connection to database...")
        try:
            await self.db.close()
            print("✅ • Connection to database closed.")
        except Exception as e:
            print(f"❌ • Failed to close connection to database")
            print(e)
        
        print("✅ • Connection to Discord closed.")

    
    # async def load_config(self) -> None:
    #     # Load the config from the database
    #     guild_id = 678607632692543509
    #     self.config.DEFAULT_PREFIX = await self.db.field(f"SELECT DEFAULT_PREFIX FROM {self.db.schema}.system WHERE GUILD_ID = $1", guild_id)