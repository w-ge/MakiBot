# Setup

In order to run MakiBot, you will need to copy your Discord Bot's Token and a Riot API key into a <code>.env</code> file in the root directory. 

Example
```
RIOT_KEY="${YOUR_RIOT_KEY}"
BOT_KEY="${YOUR_BOT_TOKEN}"
```

Then run bot.py to start the bot

</br>

# MakiBot Commands

## Login
```
$login summoner_name

Example:
$login BardMain123
```
- `To connect your account to MakiBot, you must use the login command.` Without logging in you will not be able to use any commands

## Show

```
$show summoner_name

Example
$show BardMain123
```
- Displays the most recent game of the specified summoner

## Train

```
$train
```
- Uses your most recent League of Legends game to level up the champion you played that match. 
- Your in-game stats will also be displayed for your friends to see

## ShowChamp

```
$showchamp champion_name

Example
$showchamp Bard
```
- Displays the stats of the specified champion

## Battle

```
$battle @opponent your_champ their_champ

Example:
$battle @Sushi_Man Bard Veigar
```
- Battles your specified champion with their specified champion