monitor is a little script for monitoring URLs and then reporting any failures
by email. It's not meant to be general purpose, it's just meant for me :-) But
if you find it useful obviously feel free to take it and modify it. Maybe at
some point it would be good to put the configuration in a yaml file or
something...

When you run monitor.py you must make sure SMTP_PASSWORD is set in the
environment.  You can do this in cron like so:

    0 * * * * SMTP_PASSWORD="MY_PASSWORD" /home/ed/Projects/monitor/monitor.py

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

Each site must have a `name` and a `url`.

If `cache_bust` is set to True then a uniquequery string will be attached to
the url to prevent a cache from reporting it as ok.

If `check` is supplied it will use the function to determine if the response
was ok. In this case it's attempting to parse a JSON response and check the
length of the data structure. If no `check` is supplied the response will just
be checked that it is 200 OK.

If any of the checks fail an email is sent.
