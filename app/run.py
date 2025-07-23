from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)


print("This is in Development, and testing phase")