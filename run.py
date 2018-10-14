from flask import Flask, request, render_template, redirect
from get_food import get_recipe
import requests, os

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

@app.route("/")
def hello():
    return render_template('index.html')


@app.route("/get_recipe", methods=['GET', 'POST'])
def get_recipes():
    if request.method == 'GET':
        return redirect('/')
    elif request.method == 'POST':
        print(request.form['flag'])
        if request.form['flag'] == 'url':
            myURL = request.form["MediaUrl0"]
            print(myURL)
            if myURL == '':
                return redirect('/')
            else:
                req = requests.get(myURL.strip())
                image_url = req.url
                recipes = get_recipe(image_url, filename=None, flag='url')
        else:
            '''if not request.data:
                return redirect('/')'''
            file = request.files['pic']
            print(file)
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('file uploaded successfully')
            recipes = get_recipe(filename=filename, flag='image')
        return render_template('index.html', recipes=recipes, display=len(recipes))


if __name__ == "__main__":
    app.run(debug=True)
    app.config['TEMPLATES_AUTO_RELOAD'] = True

