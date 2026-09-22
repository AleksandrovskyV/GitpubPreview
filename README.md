<br><br>
  
## Gitpub Preview:

Плагин для Sublime Text build 4200  
Для локального просмотра создаваемой гитхабом HTML по Markdown  
c `jekyll-theme-primer.css` через запрос к `GitHub-Api`  

#### Зачем?

<details><summary>Ну...</summary>

Я держу часть своих заметок в формате `.md` файлов, которые Github любезно  
превращает в публичные `.html` через базовый движок Jekyll, подключая к ним  
свою стандартную белую `.css` тему  

При вёрстке текста, я хаотично раскидываю \<br\> метки, наблюдая результат  
после каждого `push` из `Github Desktop`, глупо насилуя сервер за океаном  
Думал найти решение, чтобы смотреть файлы локально, поэтому искал плагин  
к установленому на моём ПК Sublime Text build 4200  

Первый, что попался мне под руку это `MarkdownEnhancedPreview`,  
но установить его через `Package Control` у меня не получилось и я "не" знаю причины...  
Пришлось найти сборку (уже не помню, где я её нашёл) и внедрить самостоятельно в  
`...\AppData\Roaming\Sublime Text\Packages\MarkdownPreviewEnhanced`  
Прямо со старта он дал мне возможность лицезреть html, через `ctrl+shift+p`.  
Это было круто!  

Но прошло немного времени как я понял, что вёрстка знатно отличается.  
Зная что в настройках плагина есть опция "custom_css", я решил вставить туда .css  
от Jekyll, тупо сохранив как файл и вставив до него путь)  

Две попытки, поиск и осознание, что это так не работает)))  


Пораскинув мозгами, я полез в `google` за альтернативой. Он предложил  
[`MarkdownPreview`](https://facelessuser.github.io/MarkdownPreview) что может работать через GitHub-Api, что присылает  
ответом .html на посланный ему .md  

Думаю, что GitHub-Api в разы легче, чем build через каждое слово,  
я пошёл накатывать различные релизы этого плагина с гитхаба, но моя консоль  
разрывалась от ошибок Python (несоответствие версий). Чувствуя гигантскую лень  
разбираться в этих соплях, решил раскинуть мозги, но уже у AI  

В итоге за час мы собрали плагин под мой билд Sublime Text.  
Он берёт github token > запрос к `GitHub-Api` > берёт из его ответа body>  
создаёт .html в своей папке, подключая к нему кастомный .css файл  
\* тот самый, что мы качали, с исходной страницы...  

</details><br>
  
... То есть буквально `ctrl+shift+p` > gitpub... Enter!  

Внезапное открытие браузера, и та самая, нужная мне html страница!  


#### Куда cкинуть плагин:  
C:\\Users\\...\\AppData\\Roaming\\Sublime Text\\Packages\\GitpubPreview  

#### Github токен:  

Создаёте `Simple Token` с любым именем  
и оставляете все чекбоксы пустыми  
<https://github.com/settings/tokens>  


Полученный токен `ctrl+c` и в Sublime:  
\[ top menu \] > `Preferences` > Package Settings > `GitPub Preview` > Settings  
ищем поле токена `ctrl+v` 

#### Структура:  
```
GitpubPreview\  
  ├─assets\  
  │   ├─ gitpub_md_os.py          # прототип на уровне OS  
  │   └─ jekyll-theme-primer.css  # дефолтный css файл  
  │  
  ├─ Default.sublime-commands     # регистрация ctrl+shift+p  
  ├─ Main.sublime-menu            # регистрация menu>preferences>Gitpub Preview  
  │  
  ├─ gitpub_md.sublime-settings   # config c токеном и путём к css  
  ├─ gitpub_md.py                 # логика py скрипта  
  │  
  └─ README.md                    # ты это уже прочитал...  
```