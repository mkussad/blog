from website import create_app

if __name__ == "__main__":
    # Create and run the Flask app
    app = create_app()
    app.run(debug=True)