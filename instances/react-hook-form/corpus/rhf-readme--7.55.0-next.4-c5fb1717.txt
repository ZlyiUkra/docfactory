# React Hook Form README 7.54.2 … 7.55.0-next.4
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/de88d4fafc737146f49b9559694cc59be185e9fe/README.md
# отримано: 2026-09-26
# версія: 7.55.0-next.4, 7.55.0-next.3, 7.55.0-next.2, 7.55.0-next.1, 7.55.0-next.0, 7.54.2

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
