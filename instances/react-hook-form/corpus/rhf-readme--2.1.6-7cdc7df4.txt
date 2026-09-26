# React Hook Form README 2.1.3 … 2.1.6
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/a1ecd0e25414f0498a61d8aa4e2bda492f7451ad/README.md
# отримано: 2026-09-26
# версія: 2.1.6, 2.1.5, 2.1.4, 2.1.3

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
  console.log(errors)

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input name="firstname" ref={register} />
      <input name="lastname" ref={register({ required: true })} />
      <input name="age" ref={register({ pattern: /\d+/ })} />
      <input type="submit" />
    </form>
  )
}

```
