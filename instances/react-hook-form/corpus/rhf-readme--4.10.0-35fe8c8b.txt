# React Hook Form README 4.9.0-beta.1 … 4.10.0
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/c5585d55a1e87b12d6d66a4e369eae1f3fb42f1a/README.md
# отримано: 2026-09-26
# версія: 4.10.0, 4.9.9-beta.3, 4.9.9-beta.2, 4.9.9-beta.1, 4.9.8, 4.9.8-beta.2, 4.9.8-beta.1, 4.9.7, 4.9.6, 4.9.5, 4.9.4, 4.9.4-beta.3, 4.9.4-beta.2, 4.9.4-beta.1, 4.9.3, 4.9.3-beta.3, 4.9.3-beta.2, 4.9.3-beta.1, 4.9.2, 4.9.1, 4.9.0, 4.9.0-beta.1

Performant, flexible and extensible forms with easy to use validation.

npm downloads
npm
dep
npm
Coverage Status

Tweet Join the community on Spectrum

🇦🇺English | 🇨🇳 简体中文 | 🇯🇵 日本語 | 🇰🇷한국어 | 🇫🇷Français | 🇮🇹Italiano | 🇧🇷Português | 🇪🇸Español | 🇷🇺Русский

## Features

- Built with performance and DX in mind
- Embrace uncontrolled form validation
- Improve controlled form's performance
- Tiny size without any dependency
- Follows HTML standard for validation
- Compatible with React Native
- Supports Yup, Joi, Superstruct or custom
- Supports native browser validation
- Build forms quickly with the form builder

## Install

    $ npm install react-hook-form

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

## Backers

Thanks goes to all our backers! [Become a backer].

## Contributors

Thanks goes to these wonderful people. [Become a contributor].
