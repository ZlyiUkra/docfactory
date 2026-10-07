# React Hook Form README 7.34.0 … 7.35.0-next.0
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/bb6e914ed60a604f1b1b1243224df11ac079c0b4/README.md
# отримано: 2026-09-26
# версія: 7.35.0-next.0, 7.34.2, 7.34.1, 7.34.0

https://user-images.githubusercontent.com/10513364/152621466-59a41c65-52b4-4518-9d79-ffa3fafa498a.mp4

npm downloads
npm
npm
Discord

  Get started |
  API |
  Examples |
  Demo |
  Form Builder |
  FAQs

### Features

- Built with performance, UX and DX in mind
- Embraces native HTML form validation
- Out of the box integration with UI libraries
- Small size and no dependencies
- Support Yup, Zod, AJV, Superstruct, Joi, Vest, class-validator, io-ts, nope and custom build

### Install

    npm install react-hook-form

### Quickstart

```jsx
import React from 'react';
import { useForm } from 'react-hook-form';

function App() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const onSubmit = (data) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('firstName')} />
      <input {...register('lastName', { required: true })} />
      {errors.lastName && <p>Last name is required.</p>}
      <input {...register('age', { pattern: /\d+/ })} />
      {errors.age && <p>Please enter number for age.</p>}
      <input type="submit" />
    </form>
  );
}
```

### Sponsors

Thanks go to these kind and lovely sponsors (companies and individuals)!

<a
    target = _blank
    href = 'https://wantedlyinc.com'
/>
    <img
        width = 94
        src = 'https://images.opencollective.com/wantedly/d94e44e/logo/256.png'
    />

<a
    target = _blank
    href = 'https://underbelly.is'
/>
    <img
        width = 94
        src = 'https://images.opencollective.com/underbelly/989a4a6/logo/256.png'
    />

<a
    target = _blank
    href = 'https://leniolabs.com'
/>
    <img
        width = 94
        src = 'https://images.opencollective.com/leniolabs_/63e9b6e/logo/256.png'
    />

<a
    target = _blank
    href = 'https://graphcms.com'
/>
    <img
        width = 94
        src = 'https://avatars.githubusercontent.com/u/31031438'
    />

<a
    target = _blank
    href = 'https://kanamekey.com'
/>
    <img
        width = 94
        src = 'https://images.opencollective.com/kaname/d15fd98/logo/256.png'
    />

<a
    target = _blank
    href = 'https://feathery.io'
/>
    <img
        width = 94
        src = 'https://images.opencollective.com/feathery1/c29b0a1/logo/256.png'
    />

<a
    target = _blank
    href = 'https://getform.io'
/>
    <img
        width = 94
        src = 'https://images.opencollective.com/getformio2/3c978c8/avatar/256.png'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/42376060'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/35668113'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/5726140'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/4017964'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/3655410'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/3356720'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/609452'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/279251'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/10728145'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/5763108'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/2625371'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/2098777'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/1541093'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/1481077'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/1254942'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/1087002'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/784953'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/599247'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/2566818'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/32602795'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/10023615'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/10325111'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/44457064'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/19571028'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/44406870'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/302437'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/22125223'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/2079598'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/2396344'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/1953965'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/41862257'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/43356139'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/1137112'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/2914170'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/45594821'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/5769153'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/12868063'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/459267'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/1941348'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/12888685'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/22803185'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/36793907'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/40028548'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/16930958'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/2019893'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/5480441'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/28400709'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/41503068'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/699616'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/47701145'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/4616705'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/10516382'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/548371'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/42692074'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/34721312'
    />

    <img
        width = 45
        src = 'https://avatars.githubusercontent.com/u/8176422'
    />

### Backers

Thanks go to all our backers! [Become a backer].

### Contributors

Thanks go to these wonderful people! [Become a contributor].

### Helpers

Thank you for helping and answering questions from the community.

    <img
        width = 25
        src = 'https://avatars.githubusercontent.com/u/18494222'
    />

    <img
        width = 25
        src = 'https://avatars.githubusercontent.com/u/44762180'
    />

    <img
        width = 25
        src = 'https://avatars.githubusercontent.com/u/153625'
    />

    <img
        width = 25
        src = 'https://avatars.githubusercontent.com/u/4386964'
    />

    <img
        width = 25
        src = 'https://avatars.githubusercontent.com/u/47841501'
    />

    <img
        width = 25
        src = 'https://avatars.githubusercontent.com/u/46647496'
    />

    <img
        width = 25
        src = 'https://avatars.githubusercontent.com/u/54803528'
    />

    <img
        width = 25
        src = 'https://avatars.githubusercontent.com/u/31392256'
    />

    <img
        width = 25
        src = 'https://avatars.githubusercontent.com/u/44376'
    />

    <img
        width = 25
        src = 'https://avatars.githubusercontent.com/u/16290753'
    />

### Organizations

Thanks go to these wonderful organizations! [Contribute].
