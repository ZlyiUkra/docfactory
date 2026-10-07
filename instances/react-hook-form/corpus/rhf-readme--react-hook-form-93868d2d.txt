# React Hook Form README 0.0.13 … 0.0.14
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/586810b6fa5c5985e2f276a5707bcb34fcf079aa/README.md
# отримано: 2026-09-26
# версія: 0.0.14, 0.0.13

> React hook form management without the hassle

Tweet CircleCI Coverage Status npm downloads
npm
npm

- Super easy to create forms and integrate
- Build with React hook, performance and developer experience in mind
- Follow html standard for validation
- Tiny size without other dependency 2 kB (minified + gzipped)
- Build a quick form with form builder

## Install

    $ npm install react-forme

## Website

- Get started
- API
- Demo
- Form Builder

## Quickstart

```jsx
import React from 'react';
import useForm from 'react-hook-form';

function App() {
    const { register, handleSubmit, errors } = useForm();
    const onSubmit = (data) => { console.log(data); }
    console.log(errors);

    return <form onSubmit={handleSubmit(onSubmit}>
        <input name="firstname" ref={(ref) => register({ ref, required: true })} />
        <input name="lastname" ref={(ref) => register({ ref, pattern: "[a-z]{1,15}" })} />
        <input type="submit" />
    </form>
}

```
