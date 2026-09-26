# React Hook Form README 0.1.0 … 0.3.0
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/3764cecd046caccc0a1ed7175f234c70336bea46/README.md
# отримано: 2026-09-26
# версія: 0.3.0, 0.3.0-beta.2, 0.3.0-beta.1, 0.2.0, 0.2.0-beta.2, 0.2.0-beta.1, 0.1.11, 0.1.10, 0.1.9, 0.1.8, 0.1.7, 0.1.6, 0.1.5, 0.1.4, 0.1.3, 0.1.2, 0.1.1, 0.1.0

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
