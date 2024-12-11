from qasync import QEventLoop
import asyncio

if __name__ == "__main__":
    import sys
    from package.app import app
    from db.connect_db import ConnectDB

    db = ConnectDB()
    db.init_tables()
    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    event_loop.run_until_complete(app_close_event.wait())
    event_loop.close()