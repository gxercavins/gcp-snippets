# Workflow API

The latest Dataprep releases incorporate a new [API](https://cloud.google.com/dataprep/docs/html/API-Workflow---Run-Job_145281449) to allow for programmatic access. How do we access the Workflow API? Originally written as an [answer](https://stackoverflow.com/a/59240362/6121516) to this StackOverflow question. 

## Example

When we open the Dataprep Console and navigate to the `Settings > Access Tokens` section we can click on `Generate New Token`. This will bring up the token, that you can copy to clipboard or safely store it, but also the instructions on which base endpoint to use:

---

[![enter image description here][1]][1]

Then, upon clicking on a particular Recipe (see image below) the URL in the browser will display a link in the following format:

```
https://clouddataprep.com/flows/<FLOW_ID>?recipe=<RECIPE_ID>&tab=recipe
```

[![enter image description here][2]][2]

We'll keep `RECIPE_ID>` so that our request body (`dataprep-request.json`) is something like this:

```js
{
  "wrangledDataset": {
    "id": <RECIPE_ID>
  }
}
```

Then, we can call [`JobGroups Create`](https://cloud.google.com/dataprep/docs/html/API-JobGroups-Create-v4_145281446):

```bash
curl https://api.clouddataprep.com/v4/jobGroups \
  -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @dataprep-request.json
```

The response will be similar to this output (use `python3 -m json.tool` to pretty print the JSON):

```js
{
    "sessionId": "<SESSION_ID>",
    "reason": "JobStarted",
    "jobGraph": {
        "vertices": [
            4479390,
            4479391
        ],
        "edges": [
            {
                "source": 4479390,
                "target": 4479391
            }
        ]
    },
    "id": <JOB_GROUP_ID>,
    "jobs": {
        "data": [
            {
                "id": 4479390
            },
            {
                "id": 4479391
            }
        ]
    }
}

```

Now, with the retrieved `<JOB_GROUP_ID>` we can use the [`JobGroups Get`](https://cloud.google.com/dataprep/docs/html/API-JobGroups-Get-v4_145281447) endpoint:

```bash
curl https://api.clouddataprep.com/v4/jobGroups/<JOB_GROUP_ID> \
  -H "Authorization: Bearer $TOKEN"
```

Response:

```js
{
    "id": <JOB_GROUP_ID>,
    "name": null,
    "description": null,
    "ranfrom": "ui",
    "ranfor": "recipe",
    "status": "InProgress",
    "profilingEnabled": true,
    "runParameterReferenceDate": "2019-12-08T21:49:33.000Z",
    "createdAt": "2019-12-08T21:49:35.000Z",
    "updatedAt": "2019-12-08T21:49:36.000Z",
    "workspace": {
        "id": REDACTED
    },
    "creator": {
        "id": REDACTED
    },
    "updater": {
        "id": REDACTED
    },
    "snapshot": {
        "id": 4226057
    },
    "wrangledDataset": {
        "id": <RECIPE_ID>
    },
    "flowRun": null
}
```


  [1]: https://i.stack.imgur.com/Csadb.png
  [2]: https://i.stack.imgur.com/PKUjY.png

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
