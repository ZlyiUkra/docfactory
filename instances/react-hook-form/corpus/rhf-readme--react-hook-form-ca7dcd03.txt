# React Hook Form README 7.55.0-next.5 … 7.56.0
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/3a968fed139b2c3c08b01396f2592ddd26d8eb9c/README.md
# отримано: 2026-09-26
# версія: 7.56.0, 7.56.0-next.0, 7.55.0, 7.55.0-next.9, 7.55.0-next.8, 7.55.0-next.7, 7.55.0-next.6, 7.55.0-next.5

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

Thanks go to these kind and lovely sponsors!

### Past sponsors

### Backers

Thanks go to all our backers! [Become a backer].

### Contributors

Thanks go to these wonderful people! [Become a contributor].

Documentation website supported and backed by Vercel
