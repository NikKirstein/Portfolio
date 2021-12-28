1. Must have all dependencies installed.  (mitmproxy, bs4 (beautifulSoup), sqlite, any other packages we use in import)
2. To run, be in the directory of the project, then run "Python TOBI.py", this should be run with python3.
3. Presented with options 1-5.  Run option 1 FIRST to generate an out_dump file that is used when building the database.  It should run an instance of mitmdump that logs all headers in bash.  CTRL-C to exit this bash instance and return to the main menu.
4. This entire program is controlled by TOBI.py with calling bash scripts that run inside their own bash shells.  CTRL-C to end any of the options will return you to the main menu.  It is ok to ctrl-c whenever.  If you ctrl-c while in the main menu, the program/script ends.
5. Option 2 creates a database of headers from the out_dump file.
6. Option 3 replaces current headers with headers from out_dump. We are replacing our own headers with headers from the database (also our own), so it's mostly to show that we can replace the headers from a database.  In the future, the database and option 1 of this program would collect data from a different user. (also ran into last minute bugs so this option might not be operational)
7. Option 4 injects javascript to spoof certain values.  Right now it's hardcoded to replace the userAgent to be a blackberry and the canvas size to be a specific size (that isn't a blackberry screen).  In the future, we can concantiate the string of javascript code with variables from the database call and basically spoof any property we want.  Visit browserleaks.com/javascript and see the spoofed values (should be userAgent and canvas size only at this time).
8. Option 5 does both in theory.  As stated earlier, replacing headers is a little bugged but the code is there and the javascript injection should still work.

tl;dr
Base script calls other scripts using bash so each "option" is run as a separate shell.  CTRL-C to get out of each option brings you back to the main menu.
