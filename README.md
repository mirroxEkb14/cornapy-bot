## Live Demo
<img src="https://github.com/mirroxEkb14/cornapy-bot/blob/master/utils/bot_demo.gif"/>

## About bot
> «Cinema therapy is the use of cinema or movies to manage medical, mental health, and life management». :copyright:Wikipedia

As far as wikipedia definition goes, the bot's aim is not to just offer some random movies or series to users, but do it smart, considering their preferences like mood or genre, considering their past experience and help them to escape from the state they don't want to be into by cinema

## Programming stuff
CornapyBot is
<ul>
  <li>using aiogram library<a href="https://docs.aiogram.dev/en/latest"><img alt="aiogram_logo" src="https://github.com/mirroxEkb14/cornapy-bot/blob/master/utils/aiogram_logo.png" width="15" height="15"></a></li>
  <li>running on Heroku<a href="https://en.wikipedia.org/wiki/Heroku"><img alt="heroku_logo" src="https://github.com/mirroxEkb14/cornapy-bot/blob/master/utils/heroku_logo.png" height="15"></a></li>
  <li>supporting two languages (<a href="https://en.wikipedia.org/wiki/United_States"><img alt="us_flag" src="https://github.com/mirroxEkb14/cornapy-bot/blob/master/utils/us_flag.png" height="15"></a> <a href="https://en.wikipedia.org/wiki/Russia"><img alt="us_flag" src="https://github.com/mirroxEkb14/cornapy-bot/blob/master/utils/ru_flag.png" height="15"></a>)</li>
</ul>

## Code upgrating
Some code parts that could be upgrated I left as it is on purpose, i.e. it's my first big project and I want it to be something like a cheat sheet from my future ones. For instance, after my Java experience I couldn't help but use Enum classes for containing the data. Comments help me to navigate through the whole project, though they shouldn't be in a release version

_**Class ```Enum```**_
<br>
&nbsp;&nbsp;&nbsp;&nbsp;\- could be changed to <i>dict</i> or <i>list</i>

<dl>
  <dt>
    <dd>
      from
    </dd>
  </dt>
</dl>
  
```py
from enum import Enum
class Novelty(Enum):
  OLD = 2010
  MODERN = 2011
```

<dl>
  <dt>
    <dd>
      to
    </dd>
  </dt>
</dl>

```py
NOVELTY = {
  'OLD': 2010
  'MODERN': 2011
}
```

<dl>
  <dt>Comments</dt>
    <dd>- should be omitted when publishing the project</dd>
</dl>

_**Library ```dotenv```**_<a href="https://pypi.org/project/python-dotenv"><img alt="aiogram_logo" src="https://github.com/mirroxEkb14/cornapy-bot/blob/master/utils/pypi_logo.png" width="15" height="15"></a>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;\- the tokens and ids shouldn't be got just using python I/O methods (how it is now), but using special libraries:

```py
# .env file
BOT_TOKEN=1234567899:ABC--DEFGHigKLmnOpkr9StU9vWXYZZzZZZ

# code
from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
```

_**Bot commands**_ 
<br>
&nbsp;&nbsp;&nbsp;&nbsp;\- when user changes the language, it doesn't change for commands, it's always English 
<br> 
&nbsp;&nbsp;&nbsp;(bot commands are: ```/start```, ```/help```, etc.)

## Features
Admin mode
- using ```!admin``` command, if your telegram id is added to the .env file

## Notes
- .env file; contains bot token and admins' telegram ids like:

```
BOT_TOKEN=1234567899:ABC--DEFGHigKLmnOpkr9StU9vWXYZZzZZZ
ADMIN1_TG_ID=123456789
ADMIN2_TG_ID=1234567890
```

- ```!admin```; in admin mode when admin accepts a movie from offers, in the database you need to enter ```eng_name``` and ```eng_link``` manually, because default value is ```None```, so that user doesn't have to look for and enter these values and his life is simplier

- version; v. November 2022
