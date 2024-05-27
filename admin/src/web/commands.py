from src.core import database
from src.core import seeds


def register(app):
    # AGREGA COMANDOS A FLASK
    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()

    @app.cli.command(name="seedsdb")
    def seedsdb():
        seeds.run()
        print("✅ Done!")

    @app.cli.command(name="refreshdb")
    def refreshdb():
        database.reset_db()
        seeds.run()
