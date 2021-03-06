**mypingdomr.py** is a little script for monitoring URLs with email and cron.
It's not meant to be general purpose, it's just meant for me :-) But if you find
it useful obviously feel free to take it and modify it.  Maybe at some point it
would be good to put the configuration in a yaml file or something. I'm sure
there are better more usefu utilities out there like this, but I wanted to write
my own so I knew exactly how it worked, and what its operating environment was.

When you run mypingdom.py you must make sure SMTP_PASSWORD is set in the
environment.  You can do this in cron like so:

    0 * * * * SMTP_PASSWORD="MY_PASSWORD" /home/ed/Projects/mypingdom/mypingdom.py

Configure the sites list with the list of URLs to monitor.

    sites = [
      {
        'name': 'mith',
        'url': 'https://mith.umd.edu',
        'cache_bust': True
      },
      {
        'name': 'docnow',
        'url': 'https://demo.docnow.io/api/v1/world',
        'check': lambda resp: len(json.load(resp)) > 0
      }
    ]

A few things to note:

* Each site must have a `name` and a `url`.
* If `cache_bust` is set to True then a unique query string will be appended to 
  the url to prevent a cache from reporting it as ok.
* If `check` is supplied it will use the function to determine if the response
  was ok. In this case it's attempting to parse a JSON response and check the
  length of the data structure.
* If no `check` is supplied the response will just be checked to ensure it is
  200 OK.

