from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to a secure key in production
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'csv', 'html'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def modify_html(html_content):
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove the `data-mce-fragment="1"` attribute from all tags
    for tag in soup.find_all(attrs={"data-mce-fragment": "1"}):
        del tag['data-mce-fragment']

    # Add `id` attribute to <h2> tags based on the text inside the preceding <span>
    for h2 in soup.find_all('h2'):
        span = h2.find('span')
        if span:
            span_text = span.get_text(strip=True).replace(' ', '_').replace('&nbsp;', '')
            h2['id'] = span_text

    return soup.prettify()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            modified_html = modify_html(html_content)
            return render_template('index.html', modified_html=modified_html)
    return render_template('index.html', modified_html='')

if __name__ == '__main__':
    app.run(debug=True)
