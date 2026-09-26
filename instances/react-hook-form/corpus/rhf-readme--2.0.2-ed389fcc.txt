# React Hook Form README 2.0.2
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/a5924f4371c90a6bdd1e11c12cf28266310386a2/README.md
# отримано: 2026-09-26
# версія: 2.0.2

> React hook form validation without the hassle

Tweet CircleCI Coverage Status npm downloads
npm
npm
Donate

- Super easy to create forms and integrate
- Build with React hook, performance and developer experience in mind
- Follow html standard for validation
- Tiny size without other dependency 2 kB (minified + gzipped)
- Build a quick form with form builder

## Install

    $ npm install react-hook-form

## Website

- Get started
- API
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
      <input name="lastname" ref={register({ pattern: "[a-z]{1,15}" })} />
      <input type="submit" />
    </form>
  )
}

```
