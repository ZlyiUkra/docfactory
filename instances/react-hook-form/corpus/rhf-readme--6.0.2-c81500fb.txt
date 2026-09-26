# React Hook Form README 6.0.1 … 6.0.2
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/a4095c480791563eb298ad1e9c8df4ba05bc99e1/README.md
# отримано: 2026-09-26
# версія: 6.0.2, 6.0.1

Performant, flexible and extensible forms with easy to use validation.

npm downloads
npm
npm
Coverage Status

English | 简体中文 | 日本語 | 한국어 | Français | Italiano | Português | Español | Русский | Deutsch | Türkçe

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
  const { register, handleSubmit, errors } = useForm(); // initialise the hook
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
