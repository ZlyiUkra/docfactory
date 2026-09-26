# React Hook Form README 7.36.0 … 7.37.0-next.0
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/274023d1ef068b7bfd47fd1c7010c18c42e1547b/README.md
# отримано: 2026-09-26
# версія: 7.37.0-next.0, 7.36.1, 7.36.0

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

  return (
    <form onSubmit={handleSubmit(data => console.log(data))}>
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

Thanks go to these kind and lovely sponsors!

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

### Backers

Thanks go to all our backers! [Become a backer].

### Contributors

Thanks go to these wonderful people! [Become a contributor].
