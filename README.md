# hugo_themes_report
By running this script you get a report with:
* Stars for each Theme
* Name of the Theme
* Name of the Repo owner
* Date of the latest commit  

A Bash Script to Generate a Report and Rank Hugo Themes

The website for the themes for the Hugo Static Site
generator, don't tell you how popular, or how recently-updated
the themes are. But this bash script will parse the github
api, and generate a little report for you with the
number of stars, theme name, and date of most recent
commit.

But you'll need to set up a cron job, because you'll
run into the github api limit if you try to look up
info on all 172 themes at once.

## Here's how you would set up a cron on Ubuntu 16.04
You'll need to figure out what is your PATH.
```bash
echo $PATH
```
And then you'll want to export your EDITOR, because
the `crontab -e` command invokes whatever editor
you have specified in your environment. i.e. for
vim `export EDITOR=vim` or add `export EDITOR=vim`
to `.bashrc`, (and then . your bashrc again or
restart bash).

The command to edit cron is `crontab -e`, and here's 
what a cron that runs once an hour, at ten minutes
after the hour looks like. The new cron won't exist until
you save AND close the editor, just saving the file isn't enough.

```conf
#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
10 * * * * /home/<your user name>/bin/rank_hugo_themes.bash
```

Makes sure you make the script executable.

```bash
chmod 755 ~/bin/rank_hugo_themes.bash
```

The raw output, represents what the report looks like in your terminal.

https://raw.githubusercontent.com/TrentSPalmer/hugo_themes_report/master/example_output
