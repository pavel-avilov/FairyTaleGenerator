from threading import Thread

from flask import Flask, render_template, request, flash, jsonify
from generator import generate_fairy_tale

app = Flask(__name__)
app.config["SECRET_KEY"] = "adasidnoasdlaskdasd"

th = Thread()
finished = False
tale = ""


@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/", methods=['POST'])
def generate_tale():
    if request.method == 'POST':
        start_story = request.form.get("start-story")
        if len(start_story) == 0:
            flash("Введите начало истории", "error")
        else:
            global th
            global finished
            finished = False
            if not th.is_alive():
                th = Thread(target=generate_tale_task, kwargs={'value': start_story})
                th.start()
                flash("Сказка формируется...", "success")
            else:
                flash("Дождитесь результат прошлой генерации", "error")

    return render_template("index.html")


def generate_tale_task(value):
    global tale
    global finished
    tale = generate_fairy_tale(value)
    finished = True


@app.route('/result')
def result():
    global finished
    finished = False
    return render_template("index.html", fairy_tale=tale)


@app.route('/status')
def thread_status():
    return jsonify(dict(status=('finished' if finished else 'running')))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
