# React Hook Form README 0.0.12
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/b8a4845510ab4f788d8cf7fa94e3ed1018dac454/README.md
# отримано: 2026-09-26
# версія: 0.0.12

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
import useForm from 'react-forme';

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
