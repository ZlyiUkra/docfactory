# QStash Solid.js Example
# джерело: https://github.com/upstash/qstash-js/blob/v2.12.0/examples/solidjs/README.md
# отримано: 2026-10-16
# версія: qstash-2.12.0, qstash-2.11.3, qstash-2.11.2, qstash-2.11.1, qstash-2.11.0, qstash-2.10.1, qstash-2.10.0, qstash-2.9.1, qstash-2.9.0, qstash-2.8.4, qstash-2.8.3, qstash-2.8.2, qstash-2.8.1, qstash-2.8.0, qstash-2.7.23

This example highlights how one can define an endpoint in Solid.js and make sure that only the requests coming from QStash are accepted.

To see how the endpoint is defined, see the `src/routes/api/index.ts` file.

## Local Development

To install `@upstash/qstash` in your project, run:

```
npm install @upstash/qstash
```

Then, add the environment variables `QSTASH_CURRENT_SIGNING_KEY` and `QSTASH_NEXT_SIGNING_KEY`. You can find their values from the Upstash Console.

Next, run the app with:

```
npm run dev
```

Once you have the app deployed, you can go to http://localhost:3000 and send a request to our endpoint (http://localhost:3000/api). Our request will be denied and the result will be `'Upstash-Signature' header is missing`.

To check that requests coming from QStash are accepted, we first start a local tunnel with ngrok:

```
ngrok http http://localhost:3000
```

Then, we publish a message at QStash to the ngrok endpoint (replace `NGROK_URL` and `QSTASH_TOKEN` with your own values.):

```
curl -X POST "https://qstash.upstash.io/v2/publish/<NGROK_URL>/api" \
  -H "Authorization: Bearer <QSTASH_TOKEN>" \
  -H "Content-Type: application/json" \
  -H "Upstash-Method: POST" \
  -H "Upstash-Retries: 2" \
  -H "Upstash-Forward-Custom-Header: custom-value" \
  -d '{"message":"Hello, World!"}'
```

Check the logs from QStash dashboard at Upstash Console to see that the request was completed successfully.
