# React Hook Form README 3.2.5-beta.1 … 3.5.0
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/02fd6f89d08648f50c114c452e55623bd2947249/README.md
# отримано: 2026-09-26
# версія: 3.5.0, 3.4.2, 3.4.1, 3.4.1-beta.4, 3.4.1-beta.3, 3.4.1-beta.2, 3.4.1-beta.1, 3.4.1-beta, 3.4.0, 3.3.2, 3.3.1, 3.3.0, 3.3.0-beta.1, 3.2.5, 3.2.5-beta.3, 3.2.5-beta.2, 3.2.5-beta.1

English | 简体中文

> React hook form validation without the hassle

Tweet
CircleCI
Coverage Status
npm downloads
npm
npm

- Super easy to integrate and create forms
- Built with performance and developer experience in mind
- Follows HTML standard for validation
- Tiny size without any dependency
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

## Quickstart

```jsx
import React from 'react'
import useForm from 'react-hook-form'

function App() {
  const { register, handleSubmit, errors } = useForm() // initialise the hook
  const onSubmit = (data) => { console.log(data) } // callback when validation pass

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input name="firstname" ref={register} /> {/* register an input */}

      <input name="lastname" ref={register({ required: true })} /> {/* apply required validation */}
      {errors.lastname && 'Last name is required.'} {/* error message */}

      <input name="age" ref={register({ pattern: /\d+/ })} /> {/* apply pattern validation */}
      {errors.age && 'Please enter number for age.'} {/* error message */}

      <input type="submit" />
    </form>
  )
}
```

## Contributors

Thanks goes to these wonderful people:
