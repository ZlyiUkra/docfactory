# React Hook Form README 5.7.0 … 5.7.1
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/ae82b306baf9838b6ce8200130b0ebd021744b04/README.md
# отримано: 2026-09-26
# версія: 5.7.1, 5.7.0

Performant, flexible and extensible forms with easy to use validation.

npm downloads
npm
npm
Coverage Status

Tweet Join the community on Spectrum

English | 简体中文 | 日本語 | 한국어 | Français | Italiano | Português | Español | Русский | Deutsch

## Features

- Built with performance and DX in mind
- Embrace uncontrolled form validation
- Simple integration with UI libraries
- Tiny size without any dependency
- Follows HTML standard for validation
- Compatible with React Native
- Supports Yup, Joi, Superstruct or custom
- Build forms quickly with the form builder

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
  const onSubmit = data => {
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
