# React Hook Form README 7.83.0 … 8.0.0-beta.4
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/19d06e66ad5151c439a66e2cfc88ec5f7bf2b99f/README.md
# отримано: 2026-09-26
# версія: 8.0.0-beta.4, 7.89.0, 7.88.0, 7.87.0, 7.86.0, 7.85.0, 7.84.0, 7.83.0

npm downloads
npm
npm
Discord

  Get started |
  API |
  Form Builder |
  FAQs |
  Examples

### Features

- Built with performance, UX and DX in mind
- Embraces native HTML form validation
- Out of the box integration with UI libraries
- Small size and no dependencies
- Supports Yup, Zod, AJV, Superstruct, Joi and others

### Install

    npm install react-hook-form

### Quickstart

```jsx
import { useForm } from 'react-hook-form';

function App() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <input {...register('firstName')} />
      <input {...register('lastName', { required: true })} />
      {errors.lastName && <p>Last name is required.</p>}
      <input {...register('age', { pattern: /\d+/ })} />
      {errors.age && <p>Please enter a number for age.</p>}
      <input type="submit" />
    </form>
  );
}
```

### Sponsors

We’re incredibly grateful to these kind and generous sponsors for their support!

## Major Sponsors

| Follower24 |
|---|
|  |

## Supporting Sponsors

| Thanks.dev | Kinsta | Niche | Principal | Hygraph |
|---|---|---|---|---|
|  |  |  |  |  |

### Past Sponsors

Thank you to our previous sponsors for your generous support!

|  |  |  |  |  |  |  |  |  |  |
|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
|  |  |  |  |  |  |  |  |  |  |
|  |  |  |  | | | | | | |

### Backers

Thanks go to all our backers! [Become a backer].

### Contributors

Thanks go to these wonderful people! [Become a contributor].

Documentation website supported and backed by Vercel
