# React Hook Form README 3.23.11 … 3.23.12
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/b6b06d903aa6c6dae1124f100ae18d6e7aadf0f5/README.md
# отримано: 2026-09-26
# версія: 3.23.12, 3.23.12-beta.1, 3.23.11

Performant, flexible and extensible forms with easy to use for validation.

CircleCI
npm downloads
npm
dep
npm
Coverage Status

Tweet Join the community on Spectrum

🇦🇺English | 🇨🇳简体中文

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

Thanks goes to these wonderful people:
