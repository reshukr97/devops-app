from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>DevOps Project</title>
        </head>
        <body>
            <h1>🚀 My DevOps Project</h1>

            <h2>This project currently demonstrates:</h2>

            <ul>
                <li>✅ Git & GitHub</li>
                <li>✅ Jenkins</li>
                <li>✅ Jenkins Pipeline / Groovy</li>
                <li>✅ Docker</li>
                <li>✅ Docker Hub</li>
                <li>✅ Kubernetes</li>
                <li>✅ K3s</li>
                <li>✅ Kubernetes Deployment</li>
                <li>✅ Kubernetes Service / NodePort</li>
                <li>✅ Rolling Updates</li>
                <li>✅ Jenkins → Kubernetes integration</li>
                <li>✅ CI/CD</li>
            </ul>

            <p>🎉 Deployed automatically through Jenkins!</p>
        </body>
    </html>
    """

app.run(host="0.0.0.0", port=5000)