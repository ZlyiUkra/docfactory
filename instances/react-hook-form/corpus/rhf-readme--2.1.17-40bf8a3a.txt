# React Hook Form README 2.1.17
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/598ff9662bf93875cfc56fab3411625b9dc1423c/README.md
# отримано: 2026-09-26
# версія: 2.1.17

English | 简体中文

> React hook form validation without the hassle

Tweet
CircleCI
Coverage Status
npm downloads
npm
npm

- Super easy to integrate and create forms
- Built with React Hooks with performance and developer experience in mind
- Follows HTML standard for validation
- Tiny size without other any dependency
- Build forms quickly with the form builder

## Install

    $ npm install react-hook-form

## Docs

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

      <input name="age" ref={register({ pattern: /\d+/ })} /> {/* apply a Refex validation */}
      {errors.age && 'Please enter number for age.'} {/* error message */}

      <input type="submit" />
    </form>
  )
}
```

## Contributors

Thanks goes to these wonderful people:
