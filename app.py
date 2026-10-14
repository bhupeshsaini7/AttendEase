from flask import Flask, render_template
from mysql.connector import Error as MySQLError

from config import Config
from routes.attendance import attendance_bp
from routes.dashboard import dashboard_bp
from routes.students import students_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = Config.SECRET_KEY

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(attendance_bp)

    @app.errorhandler(MySQLError)
    def handle_database_error(error):
        # Details go to the terminal, not to the visitor.
        app.logger.error("Database error: %s", error)
        return (
            render_template(
                "error.html",
                title="Database problem",
                message="Something went wrong talking to the database. "
                        "Check that MySQL is running and that your .env settings are correct.",
            ),
            500,
        )

    @app.errorhandler(404)
    def handle_not_found(error):
        return (
            render_template(
                "error.html",
                title="Page not found",
                message="The page or record you asked for does not exist.",
            ),
            404,
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)