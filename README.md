# discord-bot

Discord Bot is simple bot for your Discord server.

## Libraries

Program uses libraries
- [discord.py](https://pypi.org/project/discord.py/)
- [psycopg2](https://pypi.org/project/psycopg2/)

## PostgreSQL
Connect your PostgreSQL Database to bot which allows you to storing user's data
without database, bot still will runing but you will lost some functions

## Installation
- Install Python 3.9 + libraries that program is using (if you want all features then install PostgreSQL)
- on [discord developer side](https://discord.com/developers/applications)  create new application
- then in application go to Bot and create new bot + copy Token
- fill config.ini with token and rest information
Add your bot to the server and run:
- go to OAuth2 and click `bot` then `Administrator` and copy+paste link on internet
- run bot using `python discord-bot.py`

## Commands

### User Commands
```
top aktywnosc
```
Bot will make top 10 most active users
- Requires PostgreSQL connection

### Admin Commands

```
say <text>
```
Bot will say text instead of you

```
kick <@mention> <text>
```
Bot will kick player in first argument with reason in second argument (you have to mention player by @)

```
ban <@mention> <text>
```
Bot will ban player in first argument with reason in second argument (you have to mention player by @)


```
clear <number>
```
Bot will purge x messages on channel

## Information

Program was tested on Python 3.9.

All bugs can be reported in the "Issues" tab or on Discord of original author (Kopselek#6052).
