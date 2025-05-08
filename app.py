from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)
base_path = "json"

def load_data(file_name):
    with open(os.path.join(base_path, file_name), "r", encoding="utf-8") as f:
        return json.load(f)

def format_spec(key, value):
    if not value:
        return None
    unit_map = {
        "총길이": "m", "총폭": "m", "유효폭": "m", "높이": "m",
        "최대경간장": "m", "경간수": "개", "교통량": "대/일", "준공년도": "년"
    }
    unit = unit_map.get(key.strip())
    return f"{key.strip()}: {value} {unit}" if unit else f"{key.strip()}: {value}"

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        category = request.form.get("category")
        keyword = request.form.get("keyword", "").strip()
        file_map = {
            "교량": "bridge.json",
            "터널": "tunnel.json",
            "지하차도": "underpass.json"
        }
        if category in file_map:
            try:
                data = load_data(file_map[category])
                for item in data:
                    if keyword in item.get("시설명", ""):
                        result = {
                            "시설명": item.get("시설명", ""),
                            "주소": item.get("주소", ""),
                            "제원": []
                        }
                        for key, value in item.items():
                            if key in ["시설명", "주소"] or key.startswith("기관구분"):
                                continue
                            formatted = format_spec(key, value)
                            if formatted:
                                result["제원"].append(formatted)
                        results.append(result)
            except:
                pass
    return render_template("index.html", results=results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

