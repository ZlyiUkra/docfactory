# React Hook Form README 3.26.1 … 3.26.5
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/a6a79c5f6bf6c37ccdeba608c8d37066220cf4d3/README.md
# отримано: 2026-09-26
# версія: 3.26.5, 3.26.5-beta.7, 3.26.5-beta.6, 3.26.5-beta.5, 3.26.5-beta.4, 3.26.5-beta.3, 3.26.5-beta.2, 3.26.5-beta.1, 3.26.4, 3.26.4-beta.2, 3.26.4-beta.1, 3.26.3, 3.26.3-beta.3, 3.26.3-beta.2, 3.27.0-beta.1, 3.26.3-beta.1, 3.26.2, 3.26.2-beta.1, 3.26.1

Performant, flexible and extensible forms with easy to use for validation.

CircleCI
npm downloads
npm
dep
npm
Coverage Status

Tweet Join the community on Spectrum

🇦🇺English | 🇨🇳简体中文 | 日本語 | 🇫🇷Français | 🇰🇷한국어

## Features

- Built with performance and DX in mind
- Uncontrolled form validation
- Tiny size without any dependency
- Follows HTML standard for validation
- Compatible with React Native
- Support Yup schema-based validation
- Support browser native validation
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

Thank goes to all our backers! [Become a backer].
