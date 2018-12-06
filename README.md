# hugo_themes_report

Completely rewritten in python, using sqlite for persistent data, and using conditional github api requests to collect the data.

Finally, the script builds two (somewhat) mobile responsive reports, using a bootstrap css table.
You get a report that ranks hugo themes by number of stars, and report that ranks hugo themes
by the commit date of each theme when they are referenced as submodules in the master repo of
hugo themes.

I have the script running on a cron job, if you would like to see the result.

* [ranked by stars](http://107.161.27.86/hugo-themes-report/hugo-themes-by-num-stars.html)
* [ranked by commit date](http://107.161.27.86/hugo-themes-report/hugo-themes-by-last-commit-date.html)
* [master list of hugo themes](https://github.com/gohugoio/hugoThemes)
* [hugo themes home page](https://themes.gohugo.io/)
