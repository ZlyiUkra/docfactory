# React Hook Form README 3.21.9 … 3.21.11
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/b9a9b1e8e9d511afe9f894f34e42dfc68e41c2a4/README.md
# отримано: 2026-09-26
# версія: 3.21.11, 3.21.11-beta.1, 3.21.10, 3.21.9

English | 简体中文

Tweet
CircleCI
Coverage Status
npm downloads
npm
npm
Join the community on Spectrum

- Super easy to integrate and create forms
- Built with performance and DX in mind
- Follows HTML standard for validation
- Support browser native validation
- Tiny size without any dependency
- Uncontrolled form validation
- Build forms quickly with the form builder

## Install

    $ npm install react-hook-form

## Docs

- Motivation
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
  }; // callback when validation pass

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
