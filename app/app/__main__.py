#!/usr/bin/env python3

import asyncio

from app.main import *

loop = asyncio.get_event_loop()

app = create_app(loop)

web.run_app(app)
