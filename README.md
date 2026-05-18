A simple script that tells you who's holding up an Archipelago multiworld without having to manually pour over the spoiler file

Requires a spoiler file with full playthrough

## What does it do?

bkchecker is a host tool designed to solve one very simple problem: Everybody think's that they've runout of checks.

The script looks at the playthrough section of the spoiler log, and tells you which locations need to be checked to complete the earliest unfinished sphere.

It does not:
* Tell you which items will be found
* Tell you about anything in logic in future spheres
* Know anything about any of the games you are playing.
* Tell you about any locations that contain non-prog items.
* Tell you how/why something is in logic.


The script just goes line by line through the spoiler file, says "Sphere one is complete, sphere two is complete, oh look, Sphere three still has two checks at Brock's gym."

Use it when a game has slowed down, or people are unsure if they have more to do.
DO NOT use it to shame people.  We're all here to have fun, and randomizes sometimes have obtuse logic.  

I made this tool so I could troubleshoot an async without spoiling myself and without needing to spend far too long comparing the spoiler file against a dozen checklists. 

Please use it with kindness.

## How to use
* Install Python 3.12 or higher
* `pip install -r requirements.txt`
* `python3 bkchecker.py`

