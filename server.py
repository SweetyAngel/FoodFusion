from app import create_app

app = create_app()

def run_server():
    app.run(debug=True)

if __name__ == "__main__":
    run_server()
