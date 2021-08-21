To run these tests just type the command 
```python
python3 -m unittest
```

Or you can just run a specific file of tests

```python
python3 -m unittest test.test_title
```

Or run a specific test class in a specific file
```python
python3 -m unittest test.test_title.TestTitle
```

Or run a specific test function in a specific class in a specific file
```python
python3 -m unittest test.test_title.TestTitle.test_title_anchor
```

cron example everyday at 6am
```bash
#!/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin
0 4 * * * cd <project directory> && <rsync the db file>
0 5 * * * cd <project directory> && <rsync the html output directory>
0 6 * * * cd <project directory> && bash -c 'echo "$((python3 -m unittest)2>&1)"' | sendxmpp <sendxmpp params>
```
