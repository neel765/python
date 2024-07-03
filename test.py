from flask import Flask, request, render_template_string
import requests
from urllib.parse import urlparse

app = Flask(__name__)

# HTML template for the web page
TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Amazon 3D Model Parser</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      line-height: 1.6;
      margin: 20px;
      padding: 0;
      background-color: #f0f0f0;
    }

    h1 {
      text-align: center;
      margin-bottom: 20px;
    }

    .form-container {
      max-width: 600px;
      margin: 0 auto;
      background-color: #fff;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }

    form {
      margin-bottom: 20px;
    }

    label {
      display: block;
      margin-bottom: 10px;
    }

    input[type="text"] {
      width: 100%;
      padding: 8px;
      font-size: 16px;
      border: 1px solid #ccc;
      border-radius: 4px;
    }

    input[type="submit"] {
      background-color: #4CAF50;
      color: white;
      border: none;
      padding: 10px 20px;
      text-align: center;
      text-decoration: none;
      display: inline-block;
      font-size: 16px;
      cursor: pointer;
      border-radius: 4px;
    }

    input[type="submit"]:hover {
      background-color: #45a049;
    }

    .output {
      margin-top: 20px;
    }

    .output p {
      margin-bottom: 10px;
    }

    .output a {
      color: #0066cc;
      text-decoration: none;
    }

    .output a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <div class="form-container">
    <h1>Amazon 3D Model Parser</h1>
    <form method="POST">
      <label>Amazon URL: <input type="text" name="url" /></label>
      <input type="submit" value="Get 3D Model URL" />
    </form>
    <div class="output">
      {{ output|safe }}
    </div>
  </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            parsed_url = urlparse(url)
            host = parsed_url.netloc

            # Define supported domains
            supported_domains = [
                'www.amazon.es',
                'www.amazon.in',
                'www.amazon.com',
                'www.amazon.co.uk',
                'www.amazon.de',
                'www.amazon.co.jp',
                'www.amazon.fr',
                'www.amazon.it',
                # Add other domains as needed
            ]

            # Check if the host is in the supported domains
            if host in supported_domains:
                user_agent = 'Amazon.com/28.4.0.100 (Android/14/SomeModel)'
                cookies = '; '.join([
                    'mobile-device-info=dpi:420.0|w:1080|h:2135',
                    'amzn-app-id=Amazon.com/28.4.0.100/18.0.357239.0',
                    'amzn-app-ctxt=1.8%20%7B%22an%22%3A%22Amazon.com%22%2C%22av%22%3A%2228.4.0.100%22%2C%22xv%22%3A%221.15.0%22%2C%22os%22%3A%22Android%22%2C%22ov%22%3A%2214%22%2C%22cp%22%3A788760%2C%22uiv%22%3A4%2C%22ast%22%3A3%2C%22nal%22%3A%221%22%2C%22di%22%3A%7B%22pr%22%3A%22OnePlus7%22%2C%22md%22%3A%22GM1901%22%2C%22v%22%3A%22OnePlus7%22%2C%22mf%22%3A%22OnePlus%22%2C%22dsn%22%3A%2245ae2d3b4efa48a399e0f0a324adbaa7%22%2C%22dti%22%3A%22A1MPSLFC7L5AFK%22%2C%22ca%22%3A%22Carrier%22%2C%22ct%22%3A%22WIFI%22%7D%2C%22dm%22%3A%7B%22w%22%3A1080%2C%22h%22%3A2135%2C%22ld%22%3A2.625%2C%22dx%22%3A403.4110107421875%2C%22dy%22%3A409.90301513671875%2C%22pt%22%3A0%2C%22pb%22%3A78%7D%2C%22is%22%3A%22com.android.vending%22%2C%22msd%22%3A%22' + host + '%22%7D',
                ])

                headers = {
                    'User-Agent': user_agent,
                    'Cookie': cookies,
                }

                try:
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()
                    result = response.text
                    if 'href="/view-3d' in result:
                        model_url = result.split('href="/view-3d')[1].split('"')[0]
                        output = f'3D Model: <a target="_blank" href="https://{host}/view-3d{model_url}">https://{host}/view-3d{model_url}</a> (The zip file with the model can be found in the network tab in Developer tools)'
                    else:
                        output = 'No 3D model found.'
                except requests.RequestException as e:
                    output = f'Error retrieving the URL: {e}'
            else:
                output = 'Unsupported URL. Make sure it is a valid Amazon product URL.'
        else:
            output = 'Please enter a valid URL.'

    return render_template_string(TEMPLATE, output=output)

if __name__ == '__main__':
    app.run(debug=True)
