# League of Legends (LoL) Event Player
This is a Python program that reads from the League of Legends API to change music or play sound effects on game events.

## Main Features
- Can play custom sound effects on player death or kill
- Can change music based on current Kill-Death-Assist Ratio

## Development:
- Settings are only able to be changed by the "settings.txt" file; currently working on a more user-friendly interface
- Program is known to crash between games, especially with other modes like spectator or Teamfight Tactics; simply relaunch the program for the time being.

## About: Music
The program can keep track of multiple simulaneously-playing music tracks,
switching between them as the player's KDA ratio changes. For example,
the user can keep piano, ordinary, and remixed versions of a song, allowing
the program to change through them as the player triggers events in the game.
This is intended to suit the mood of the game, as different versions of
a song will play when the player is performing well, or poorly.

By default (might be available to customize later), if the player is
waiting for respawn, the first music track plays exclusively, while
for 10 seconds after getting or assisting in a kill, the next music track
in the KDA ratio order is played, for dynamic change in music even when
thresholds are not surpassed (a big issue when deaths are high).


## Available Settings:
- Volume control for sound effects
- Volume control for each music file separately
- Customizable KDA thresholds
