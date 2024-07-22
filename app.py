from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY_RENDER')  # Load from environment variable or use a default value
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
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
    modified_html = ''
    if request.method == 'POST':
        html_content = None

        # Check if a file is uploaded
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                with open(file_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
        
        # Check if HTML content is pasted
        elif 'html_input' in request.form and request.form['html_input'] != '':
            html_content = request.form['html_input']
        
        # Check if HTML content is in the modified HTML textarea
        elif 'modified_html' in request.form and request.form['modified_html'] != '':
            html_content = request.form['modified_html']
        
        if html_content:
            modified_html = modify_html(html_content)
            if 'save_to_file' in request.form:
                output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'modified_html.txt')
                with open(output_path, 'w', encoding='utf-8') as file:
                    file.write(modified_html)
                return send_file(output_path, as_attachment=True)
        else:
            flash('No file selected and no HTML input provided')
            return redirect(request.url)
    return render_template('index.html', modified_html=modified_html)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
