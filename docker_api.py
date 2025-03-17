from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/scale", methods=["POST"])
def scale():
    num_workers = request.json.get("num_workers", 1)
    subprocess.run(["docker", "compose", "up", "-d", "--scale", f"my-scraper-1={num_workers}"])

    return {"status": "success", "scaled_to": num_workers}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
