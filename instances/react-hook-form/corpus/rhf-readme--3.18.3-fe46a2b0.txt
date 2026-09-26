# React Hook Form README 3.17.0 … 3.18.3
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/352fa9d25146ae20391e6e1fc35be8d772f79750/README.md
# отримано: 2026-09-26
# версія: 3.18.3, 3.18.2, 3.18.1, 3.18.0, 3.17.5, 3.17.5-beat.1, 3.17.4, 3.17.3, 3.17.2, 3.17.1, 3.17.0

English | 简体中文

Tweet
CircleCI
Coverage Status
npm downloads
npm
npm

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
import React from "react";
import useForm from "react-hook-form";

function App() {
  const { register, handleSubmit, errors } = useForm(); // initialise the hook
  const onSubmit = data => { console.log(data) }; // callback when validation pass

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input name="firstname" ref={register} /> {/* register an input */}

      <input
        name="lastname"
        ref={register({ required: true })}
      />
      {errors.lastname && "Last name is required."}

      <input
        name="age"
        ref={register({ pattern: /\d+/ })}
      />
      {errors.age && "Please enter number for age."}

      <input type="submit" />
    </form>
  );
}

```

## Contributors

Thanks goes to these wonderful people:
