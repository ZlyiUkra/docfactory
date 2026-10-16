# @upstash/feedback README 0.0.3: Feedback Widget
# джерело: https://registry.npmjs.org/@upstash/feedback/-/feedback-0.0.3.tgz
# отримано: 2026-10-16
# версія: feedback-0.0.3

--summary--

## Docs

- Set up
- Configuring Upstash
- Configuring Auth0
- Deploy on Vercel

## Set up

First clone the repo. Copy the `.env.local.example` file to `.env.local` (which
will be ignored by Git):

```bash
cp .env.local.example .env.local
```

## Configuring Upstash

1. Go to the Upstash Console and create a new
   database

#### Upstash environment

`UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` find the variables in
the database details page in Upstash Console.

## Configuring Auth0

1. Go to the Auth0 dashboard and create a new
   application of type **Single Page Web Applications**
2. Go to the settings page of the application
3. Configure the following settings:
    - **Allowed Callback URLs**: Should be set to `http://localhost:3000/` when
      testing locally or typically to `https://myapp.com/` when deploying your
      application.
    - **Allowed Logout URLs**: Should be set to `http://localhost:3000/` when
      testing locally or typically to `https://myapp.com/` when deploying your
      application.
4. Save the settings.

#### Auth0 environment

- `NEXT_PUBLIC_AUTH0_DOMAIN`: Can be found in the Auth0 dashboard
  under `settings`.
- `NEXT_PUBLIC_AUTH0_CLIENT_ID`: Can be found in the Auth0 dashboard
  under `settings`.
- `NEXT_PUBLIC_AUTH0_ADMIN_ID`: This is the **user_id** of the admin user. First
  run your application and sign-in yourself. Then find your **user_id** in the
  Auth0 console, **"User Management > Users"** page.

## Replace Your Logo

Copy your logo image to `public` folder. Then edit `components/header/index.js`.

## Run Your Project

In the project folder, run:
`npm install`
`next dev`

## Deploy Your Project

To deploy your project to Vercel, run `vercel` in the project folder.

Or you can push it to GitHub/GitLab/Bitbucket
and import to Vercel
.

**Important**: When you import your project on Vercel, make sure to click on **
Environment Variables** and set them to match your `.env.local` file.
