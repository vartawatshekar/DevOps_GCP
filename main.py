from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Interactive Flask App</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                text-align: center;
            }
            .btn {
                background-color: #007bff;
                color: white;
                padding: 10px 20px;
                border: none;
                cursor: pointer;
                border-radius: 5px;
                font-size: 16px;
                transition: background-color 0.3s ease;
            }
            .btn:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hello Bhavik (Docker Version 2)! Welcome to Python Flask World</h1>
            <button class="btn" onclick="changeColor()">Change Color</button>
        </div>
        <script>
            function changeColor() {
                const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff'];
                const randomColor = colors[Math.floor(Math.random() * colors.length)];
                document.body.style.backgroundColor = randomColor;
            }
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
