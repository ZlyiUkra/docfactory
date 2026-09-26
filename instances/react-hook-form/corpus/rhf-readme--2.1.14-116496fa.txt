# React Hook Form README 2.1.7 … 2.1.14
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/1db3ef37d312a18ee45948f256c54bb4795fc8e0/README.md
# отримано: 2026-09-26
# версія: 2.1.14, 2.1.13, 2.1.13-beta.4, 2.1.13-beta.3, 2.1.13-beta.2, 2.1.13-beta.1, 2.1.12, 2.1.12-beta.3, 2.1.12-beta.2, 2.1.12-beta.1, 2.1.11, 2.1.10, 2.1.10-beta.3, 2.1.10-beta.2, 2.1.10-beta.1, 2.1.9, 2.1.8, 2.1.7

> React hook form validation without the hassle

Tweet CircleCI Coverage Status npm downloads
npm
npm

- Super easy to create forms and integrate
- Build with React hook, performance and developer experience in mind
- Follow html standard for validation
- Tiny size without other dependency 2 kB (minified + gzipped)
- Build a quick form with form builder

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
  const { register, handleSubmit, errors } = useForm()
  const onSubmit = (data) => { console.log(data) }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input name="firstname" ref={register} />

      <input name="lastname" ref={register({ required: true })} />
      {errors.lastname && 'Last name is required.'}

      <input name="age" ref={register({ pattern: /\d+/ })} />
      {errors.age && 'Please enter number for age.'}

      <input type="submit" />
    </form>
  )
}

```
