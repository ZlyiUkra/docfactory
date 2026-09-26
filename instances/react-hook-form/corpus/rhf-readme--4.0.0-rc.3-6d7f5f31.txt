# React Hook Form README 4.0.0-beta.2 … 4.0.0-rc.3
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/40b64eeb94bcdd7643e85962b007e048290ef2a7/README.md
# отримано: 2026-09-26
# версія: 4.0.0-rc.3, 4.0.0-rc.2, 4.0.0-rc.1, 4.0.0-rc.0, 4.0.0-beta.2

Performant, flexible and extensible forms with easy to use validation.

CircleCI
npm downloads
npm
dep
npm
Coverage Status

Tweet Join the community on Spectrum

🇦🇺English | 🇨🇳 简体中文 | 🇯🇵 日本語 | 🇰🇷한국어 | 🇫🇷Français | 🇮🇹Italiano | 🇧🇷Português

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
import useForm from 'react-hook-form';

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
