# React Hook Form README 2.1.0 … 2.1.2
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/4861b091abc0dfb8138b0ae872d3800a89c77279/README.md
# отримано: 2026-09-26
# версія: 2.1.2, 2.1.2-beta.2, 2.1.2-beta.1, 2.1.1, 2.1.0

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
      <input name="lastname" ref={register({ pattern: "[a-z]{1,15}" })} />
      <input type="submit" />
    </form>
  )
}

```
