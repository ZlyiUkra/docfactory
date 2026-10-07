# React Hook Form README 3.28.4 … 3.28.12-beta.3
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/8386bfa4ed4759df194a6a9a0c012df9cdf9d995/README.md
# отримано: 2026-09-26
# версія: 3.28.12-beta.3, 3.28.12-beta.2, 3.28.12-beta.1, 3.28.11, 3.28.10, 3.28.10-beta.1, 3.28.9, 3.28.8, 3.28.8-beta.1, 3.28.7, 3.28.6-beta.2, 3.28.6-beta.1, 3.28.5, 3.28.4

Performant, flexible and extensible forms with easy to use validation.

CircleCI
npm downloads
npm
dep
npm
Coverage Status

Tweet Join the community on Spectrum

🇦🇺English | 🇨🇳简体中文 | 🇯🇵日本語 | 🇰🇷한국어 | 🇫🇷Français | 🇮🇹Italiano

## Features

- Built with performance and DX in mind
- Uncontrolled form validation
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

## Contributors

Thanks goes to these wonderful people. [Become a contributor].

## Backers

Thanks goes to all our backers! [Become a backer].
