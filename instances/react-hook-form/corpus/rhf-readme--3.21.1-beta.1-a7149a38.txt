# React Hook Form README 3.20.1 … 3.21.1-beta.1
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/fea2ebb3575e8539fe00ad71f96e01aa850ebecb/README.md
# отримано: 2026-09-26
# версія: 3.21.1-beta.1, 3.21.0, 3.21.0-beta.1, 3.20.4, 3.20.4-beta.1, 3.20.3, 3.20.2, 3.20.1

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
