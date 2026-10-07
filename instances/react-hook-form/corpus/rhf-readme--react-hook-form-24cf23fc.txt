# React Hook Form README 7.61.0 … 8.0.0-alpha.5
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/e8ccff94d11ad44ffe98f7e39f2467be3774b246/README.md
# отримано: 2026-09-26
# версія: 8.0.0-alpha.5, 7.64.0, 7.63.0, 7.62.0, 7.61.1, 7.61.0

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
- Support Yup, Zod, AJV, Superstruct, Joi and others

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
      {errors.age && <p>Please enter number for age.</p>}
      <input type="submit" />
    </form>
  );
}
```

### Sponsors

We’re incredibly grateful to these kind and generous sponsors for their support!

### Past Sponsors

Thank you to our previous sponsors for your generous support!

### Backers

Thanks go to all our backers! [Become a backer].

### Contributors

Thanks go to these wonderful people! [Become a contributor].

Documentation website supported and backed by Vercel
