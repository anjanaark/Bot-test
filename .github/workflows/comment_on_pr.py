import os
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
PR_NUMBER = os.environ.get("PR_NUMBER")

def post_comment(file_path, line_number, message):
    url = f"https://api.github.com/repos/{os.environ['GITHUB_REPOSITORY']}/pulls/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "body": f"Lint issue: {message}",
        "path": file_path,
        "position": line_number,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print("Comment posted successfully")
    else:
        print(f"Failed to post comment. Status code: {response.status_code}")

def main():
    with open("lint_output.txt", "r") as f:
        lint_output = f.read()

    lines = lint_output.split('\n')
    for line in lines:
        parts = line.split(':')
        if len(parts) >= 4:
            file_path = parts[0]
            line_number = int(parts[1])
            message = ':'.join(parts[3:])
            post_comment(file_path, line_number, message)

if __name__ == "__main__":
    main()
