from flask import Flask, render_template, request, redirect

# app = Flask(__name__)
app = Flask(__name__, template_folder='./templates', static_folder='./static')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        return redirect(url_for('ShootPhoto'))
    return render_template('index.html')


@app.route('/ShootPhoto.html')
def ShootPhoto():
    return render_template('ShootPhoto.html')


if __name__ == "__main__":
    app.run()
