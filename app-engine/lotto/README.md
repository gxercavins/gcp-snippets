# Lotto Game

Modify a basic hello world example to return a number combination that conforms to the spanish [Primitiva](https://www.loteriasyapuestas.es/es/resultados/primitiva) standard. This was part of an interview I did years ago so I'll leave it as is instead of trying to improve it (i.e. using sets or using `random.choice` while popping out numbers to emulate real game behavior) or switch away from Python 2. Original code retrieved thanks to Stackdriver Debugging.

## Example

Note that the example is constructed over the official hello world sample [here](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/hello_world) using the `webapp2` framework.

We add a new handler for the `/lotto` endpoint:

```python
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/lotto', LottoPage),
], debug=True)
```

and define `LottoPage` as:

```python
class LottoPage(webapp2.RequestHandler):
    def get(self):
        lucky_combination = []
        repeat = True

	for i in range(6):
	    while (repeat):
		num = randint(1,49)
		if num in lucky_combination:
		    repeat = True
		else:
		    repeat = False  
	    lucky_combination.append(num)
	    repeat = True

	logging.info(sorted(lucky_combination))
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(sorted(lucky_combination))
```

We generate six random non-repeating numbers between 1 and 49 and return the sorted combination.

The code can be tested locally with:

```bash
dev_appserver.py app.yaml
```

as explained in the [quickstart guide](https://cloud.google.com/appengine/docs/standard/python/quickstart#test_the_application) (mind the SDK dependencies [here](https://cloud.google.com/appengine/docs/standard/python/quickstart#before-you-begin)).

Then you can navigate to `http://localhost:8080/` and get a combination such as:

![example](https://user-images.githubusercontent.com/29493411/69971425-290bd700-1520-11ea-9913-9ed3369cfc04.png)

If you deploy the service to App Engine be aware of the possible costs if the number of requests exceeds the [free tier](https://cloud.google.com/free/docs/gcp-free-tier).

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
