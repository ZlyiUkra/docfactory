# React Hook Form README 6.5.2-beta.1 … 6.8.1
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/2935dee383d073d3d4b5466e47dbdb0251ed926b/README.md
# отримано: 2026-09-26
# версія: 6.8.1, 6.8.0, 6.7.2, 6.7.1, 6.7.0, 6.6.0, 6.5.3, 6.5.2, 6.5.2-beta.1

Performant, flexible and extensible forms with easy to use validation.

npm downloads
npm
npm
Coverage Status

English | 繁中 | 简中 | 日本語 | 한국어 | Français | Italiano | Português | Español | Русский | Deutsch | Türkçe

## Features

- Built with performance and DX in mind
- Embrace native form validation
- Simple integration with UI libraries
- Tiny size without any dependency
- Follows HTML standard for validation
- Resolvers support Yup, Superstruct, Joi or custom
- Build forms quickly with Form Builder

## Install

    npm install react-hook-form

## Links

- Motivation
- Video tutorial
- Get started
- API
- Examples
- Demo
- Form Builder
- FAQs

## Quickstart

```jsx
import React from 'react';
import { useForm } from 'react-hook-form';

function App() {
  const { register, handleSubmit, errors } = useForm(); // initialize the hook
  const onSubmit = (data) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input name="firstname" ref={register} /> {/* register an input */}

      <input name="lastname" ref={register({ required: true })} />
      {errors.lastname && 'Last name is required.'}

      <input name="age" ref={register({ pattern: /\d+/ })} />
      {errors.age && 'Please enter number for age.'}

      <input type="submit" />
    </form>
  );
}
```

## Sponsors

Want your logo here? DM on Twitter

## Backers

Thanks goes to all our backers! [Become a backer].

## Organizations

Thanks goes to these wonderful organizations! [Contribute].

## Contributors

Thanks goes to these wonderful people! [Become a contributor].
