
General notes:
You should only run files with a _main.py extension

Step #1:
Run reddit_fetcher_main.py

to update the database (stored in reddit_submissions.sqlite

Step #2:
Run reddit_analyzer_main.py

to update the reddit_submissions.sqlite with the computed features (height, weight, etc)

They are called "computed features" because they are computed based off the title and
text of the reddit post

Step #3:
Run reddit_imgur_main.py

Step #4
Run reddit_dump_json_main.py

to dump the files into a .json file

Step #4
Copy the .json file into the html/ directory and run the index.html file in Firefox.
Chrome does not allow loading local .json files, so you need to run it on firefox
for now.