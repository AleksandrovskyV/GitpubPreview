import os,sys, json
import urllib.request
import urllib.error

# github classic tokens
# not check all punkts, any name
# https://github.com/settings/tokens

GITHUB_USER_TOKEN = ""

def render_markdown(config):
    github_token = config.get("github_token", "").strip()
    md_file_path = config.get("md_path", "").strip()
    css_path     = config.get("css_path", "").strip()

    if not github_token:
        print("[rndmrk] not token.")
        return

    if not md_file_path or not os.path.exists(md_file_path):
        print(f"[rndmrk] md file not found: '{md_file_path}'")
        return

    md_filename = os.path.splitext(os.path.basename(md_file_path))[0]+".md preview" 
    if not css_path or not os.path.exists(css_path):
        print(f"[rndmrk] ccs not found")

    print(f"[rndmrk] start...")

    with open(md_file_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    print("[rndmrk] start...")
    
    url = "https://api.github.com/markdown"
    data = json.dumps({"text": md_content, "mode": "markdown"}).encode("utf-8")
    
    req = urllib.request.Request(url, data=data)
    req.add_header("User-Agent", "Sublime-Local-Compiler")
    req.add_header("Authorization", f"Bearer {github_token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")

    try:
        with urllib.request.urlopen(req) as response:
            html_body = response.read().decode("utf-8")

        output_html = f"""<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8">
<title>{md_filename}</title>
<link rel="stylesheet" href="file:///{css_path}">
</head><body>
<div class="container-lg px-3 my-5 markdown-body">
<h1><a href="">{md_filename}</a></h1>
{html_body}
</div>
</body>
</html>
"""
        output_path = os.path.join(os.path.dirname(md_file_path), "preview.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_html)
        
        print(f"[rndmrk] output: {output_path}")

    except urllib.error.HTTPError as e:
        print(f"[rndmrk] error: {e.code}.")
        print(e.read().decode("utf-8", errors="ignore"))
        return
    except Exception as e:
        print(f"rndmrk] error API: {e}")
        return



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[rndmrk] from script.py")
        config = {
            "github_token": GITHUB_USER_TOKEN, # Токен
            "md_path"     : "./init.md",
            "css_path"    : "./jekyll-theme-primer.css"
        }
        render_markdown(config)
    else:
        if len(sys.argv) < 4:
            print("[rndmrk] <token> <md_path> <css_path>")
        else:
            config = {
                "github_token": sys.argv[1],
                "md_path": sys.argv[2],
                "css_path": sys.argv[3]
            }
            render_markdown(config)