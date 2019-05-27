from flask import Flask

app = Flask(__name__)


@app.route('/')
def main():

    pass

@app.route('/list')
def list():
    pass


if __name__ == '__main__':
    app.run()
