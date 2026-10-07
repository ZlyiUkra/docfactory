# React Hook Form README 3.28.3
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/784aa4af3b443f11484fac0df97458b0e22a1442/README.md
# отримано: 2026-09-26
# версія: 3.28.3

Performant, flexible and extensible forms with easy to use validation.

CircleCI
npm downloads
npm
dep
npm
Coverage Status

Tweet Join the community on Spectrum

🇦🇺English | 🇨🇳简体中文 | 🇯🇵日本語 | 🇰🇷한국어 | 🇫🇷Français

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
