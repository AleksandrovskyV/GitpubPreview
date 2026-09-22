import sublime
import sublime_plugin

import os, json, webbrowser
import urllib.request
import urllib.error

import tempfile

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
        
        use_temp = settings.get("use_temp", False)
        refresh_temp = settings.get("refresh_temp", False)
        refresh_time = settings.get("refresh_time", 2)


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

        meta_upd="""
<meta http-equiv="refresh" content="{}">
        """.format(refresh_time) if refresh_temp else ""

        try:
            with urllib.request.urlopen(req) as response:
                html_body = response.read().decode("utf-8")


            output_html = """
<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8">
{}
<title>GitPub Preview</title>
<link rel="stylesheet" href="file:///{}">
</head>
<div class="container-lg px-3 my-5 markdown-body">
<h1><a href="">{}</a></h1>
{}
</body>
</html>
            """.format(meta_upd,csslink,title,html_body)



            if use_temp:
                temp_dir = tempfile.gettempdir()
                output_path = os.path.join(temp_dir, "gitpub_preview.html")                
            else:
                res_file_name = os.path.splitext(title)[0] + "_preview.html"
                output_path = os.path.join(os.path.dirname(md_file_path), res_file_name)


            file_exists = os.path.exists(output_path)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(output_html)
            
            url_to_open = "file:///{}".format(output_path.replace(os.sep, '/'))

            if not refresh_temp:
                webbrowser.open(url_to_open, new=0)
            else:
                file_exists = os.path.exists(output_path)

                if not file_exists:
                    webbrowser.open(url_to_open, new=0)

            sublime.status_message("[GitPub] Success: {}".format(output_path))



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

