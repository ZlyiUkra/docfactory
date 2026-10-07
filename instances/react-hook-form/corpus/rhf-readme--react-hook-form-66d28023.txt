# React Hook Form README 4.1.0-beta.1 … 4.8.2
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/09e5f14823a2c9e4a16293db29d1e66946fa75e8/README.md
# отримано: 2026-09-26
# версія: 4.8.2, 4.8.1, 4.8.0, 4.7.3-beta.3, 4.7.3-beta.2, 4.7.3-beta.1, 4.7.3-next.0, 4.7.2, 4.7.2-next.0, 4.7.1, 4.7.1-beta.1, 4.7.0, 4.7.0-beta.2, 4.6.3-beta.4, 4.7.0-beta.1, 4.6.3-beta.3, 4.6.3-beta.2, 4.6.3-beta.1, 4.6.2, 4.6.2-beta.1, 4.6.1, 4.6.0, 4.5.7-beta.3, 4.5.7-beta.2, 4.5.7-beta.1, 4.5.6, 4.5.6-beta.5, 4.5.6-beta.4, 4.5.6-beta.3, 4.5.6-beta.2, 4.5.6-beta.1, 4.5.5, 4.5.4, 4.5.4-beta.2, 4.5.4-beta.1, 4.5.3, 4.5.3-beta.3, 4.5.3-beta.2, 4.5.3-beta.1, 4.5.2, 4.5.2-beta.2, 4.5.2-beta.1, 4.5.1, 4.5.1-beta.2, 4.5.1-beta.1, 4.5.0, 4.5.0-beta.12, 4.5.0-beta.11, 4.5.0-beta.10, 4.5.0-beta.9, 4.5.0-beta.8, 4.5.0-beta.7, 4.4.8, 4.4.7, 4.5.0-beta.6, 4.4.6, 4.5.0-beta.5, 4.4.5, 4.4.5-beta.3, 4.4.5-beta.1, 4.4.4, 4.5.0-beta.4, 4.4.3, 4.5.0-beta.2, 4.5.0-beta.1, 4.4.2, 4.4.1, 4.4.1-beta.1, 4.4.0, 4.3.1-beta.2, 4.3.1-beta.1, 4.3.0, 4.3.0-beta.1, 4.2.2, 4.2.2-beta.1, 4.2.1, 4.2.1-beta.1, 4.2.0, 4.1.1-beta.1, 4.1.0, 4.1.0-beta.1

Performant, flexible and extensible forms with easy to use validation.

CircleCI
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
- Supports Yup schema-based validation
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
