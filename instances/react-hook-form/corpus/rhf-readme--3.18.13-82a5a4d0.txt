# React Hook Form README 3.18.10 … 3.18.13
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/36f4e24a7b2ce6089e8bc46a55b0498289d90f4b/README.md
# отримано: 2026-09-26
# версія: 3.18.13, 3.18.12, 3.18.11, 3.18.10

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
