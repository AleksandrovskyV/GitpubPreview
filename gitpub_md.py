import sublime
import sublime_plugin

import os, json, webbrowser
import urllib.request
import urllib.error

class GitpubMdCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        md_file_path = self.view.file_name()
        
        if not md_file_path or not md_file_path.endswith(('.md', '.markdown')):
            sublime.error_message("[GitPub] Error_1 ")
            return

        settings = sublime.load_settings("gitpub_md.sublime-settings")
        sublime.status_message("[GitPub] {}".format(settings))
        github_token = settings.get("github_token", "").strip()
        css_setting = settings.get("css_path", "./assets/jekyll-theme-primer.css").strip()

        if not github_token:
            sublime.error_message("[GitPub] Error_2 'github_token' not valid")
            return

        plugin_dir = os.path.dirname(__file__)
        if css_setting.startswith("./") or css_setting.startswith(".\\"):
            css_path = os.path.join(plugin_dir, css_setting[2:])
        else:
            css_path = css_setting

        if not os.path.exists(css_path):
            sublime.status_message("[GitPub] CSS NotFound")

        sublime.status_message("[GitPub] Send Markdown in GitHub API...")

        md_content = self.view.substr(sublime.Region(0, self.view.size()))

        url = "https://api.github.com/markdown"
        data = json.dumps({"text": md_content, "mode": "markdown"}).encode("utf-8")
        
        req = urllib.request.Request(url, data=data)
        req.add_header("User-Agent", "Sublime-Local-Compiler")
        req.add_header("Authorization", "Bearer {}".format(github_token))
        req.add_header("Content-Type", "application/json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")

        title = os.path.basename(md_file_path)
        csslink = css_path.replace(os.sep, '/')
        try:
            with urllib.request.urlopen(req) as response:
                html_body = response.read().decode("utf-8")

            output_html = """
<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8">
<title>Preview: {}</title>
<link rel="stylesheet" href="file:///{}">
</head>
<div class="container-lg px-3 my-5 markdown-body">
<h1><a href="">{}</a></h1>
{}
</body>
</html>
            """.format(title,csslink,title,html_body)

            output_path = os.path.join(os.path.dirname(md_file_path), "preview.html")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(output_html)
            
            sublime.status_message("[GitPub] Succes!")
            webbrowser.open("file:///{}".format(output_path))

        except urllib.error.HTTPError as e:
            err_details = e.read().decode("utf-8", errors="ignore")
            
            if e.code == 401:
                sublime.error_message(
                    "[GitPub][Error][401]\n\n"
                    "Not valid token github \n"
                    "Check in Preferences>...>Settings\n"
                )
            else:
                sublime.error_message("[GitPub] API Error {}]\n{}".format(e.code, err_details))
                
        except Exception as e:
            sublime.error_message("[GitPub] Network Error\n{}".format(str(e)))


