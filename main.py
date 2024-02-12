# Package Imports
import asyncio

# Local Imports
from api.ui_generator import UIGenerator


async def main():
    ui_generator = UIGenerator()
    await ui_generator.generate_ui()


asyncio.run(main())
