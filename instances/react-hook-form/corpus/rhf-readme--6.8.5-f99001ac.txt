# React Hook Form README 6.8.5
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/5ed53dfd48e0cb55516d0b835d025644205439aa/README.md
# отримано: 2026-09-26
# версія: 6.8.5

Performant, flexible and extensible forms with easy to use validation.

npm downloads
npm
npm
Discord

English | 繁中 | 简中 | 日本語 | 한국어 | Français | Italiano | Português | Español | Русский | Deutsch | Türkçe

## Features

- Built with performance and DX in mind
- Embrace native form validation
- Simple integration with UI libraries
- Tiny size without any dependency
- Follows HTML standard for validation
- Resolvers support Yup, Superstruct, Joi or custom
- Build forms quickly with Form Builder

## Install

    npm install react-hook-form

## Links

- Motivation
- Video tutorial
- Get started
- API
- Examples
- Demo
- Form Builder
- FAQs

## Quickstart

```jsx
import React from 'react';
import { useForm } from 'react-hook-form';

function App() {
  const { register, handleSubmit, errors } = useForm(); // initialize the hook
  const onSubmit = (data) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input name="firstname" ref={register} /> {/* register an input */}

      <input name="lastname" ref={register({ required: true })} />
      {errors.lastname && 'Last name is required.'}

      <input name="age" ref={register({ pattern: /\d+/ })} />
      {errors.age && 'Please enter number for age.'}

      <input type="submit" />
    </form>
  );
}
```

## Sponsors

Thanks go to these kind and lovely sponsors (company and individuals)!

    <a href="https://github.com/sayav"
    ><img
            src="https://avatars1.githubusercontent.com/u/42376060?s=60&v=4"
            width="30"
            height="30"
            alt="@sayav"
    />
    <a href="https://github.com/lemcii"
    ><img
            src="https://avatars1.githubusercontent.com/u/35668113?s=60&v=4"
            width="30"
            height="30"
            alt="@lemcii"
    />
    <a href="https://github.com/washingtonsoares"
    ><img
            src="https://avatars0.githubusercontent.com/u/5726140?s=460&u=b300a6fa08a24c59b9db6ebf246384cf8b16a140&v=4"
            width="30"
            height="30"
            alt="@washingtonsoares"
    />
    <a href="https://github.com/lixunn"
    ><img
            src="https://avatars0.githubusercontent.com/u/4017964?s=460&u=3a3fdffeb97749d7509d9c5e9be2cafcb98e426f&v=4"
            width="30"
            height="30"
            alt="@lixunn"
    />
    <a href="https://github.com/SamSamskies"
    ><img
            src="https://avatars2.githubusercontent.com/u/3655410?s=60&v=4"
            width="30"
            height="30"
            alt="@SamSamskies"
    />
    <a href="https://github.com/peaonunes"
    ><img
            src="https://avatars2.githubusercontent.com/u/3356720?s=60&v=4"
            width="30"
            height="30"
            alt="@peaonunes"
    />
    <a href="https://github.com/wilhelmeek"
    ><img
            src="https://avatars2.githubusercontent.com/u/609452?s=60&v=4"
            width="30"
            height="30"
            alt="@wilhelmeek"
    />
    <a href="https://github.com/iwarner"
    ><img
            src="https://avatars2.githubusercontent.com/u/279251?s=60&v=4"
            width="30"
            height="30"
            alt="@iwarner"
    />
    <a href="https://github.com/joejknowles"
    ><img
            src="https://avatars2.githubusercontent.com/u/10728145?s=60&v=4"
            width="30"
            height="30"
            alt="@joejknowles"
    />
    <a href="https://github.com/chris-gunawardena"
    ><img
            src="https://avatars0.githubusercontent.com/u/5763108?s=60&v=4"
            width="30"
            height="30"
            alt="@chris-gunawardena"
    />
    <a href="https://github.com/Tymek"
    ><img
            src="https://avatars1.githubusercontent.com/u/2625371?s=60&v=4"
            width="30"
            height="30"
            alt="@Tymek"
    />
    <a href="https://github.com/Luchanso"
    ><img
            src="https://avatars0.githubusercontent.com/u/2098777?s=60&v=4"
            width="30"
            height="30"
            alt="@Luchanso"
    />
    <a href="https://github.com/vcarel"
    ><img
            src="https://avatars1.githubusercontent.com/u/1541093?s=60&v=4"
            width="30"
            height="30"
            alt="@vcarel"
    />
    <a href="https://github.com/gragland"
    ><img
            src="https://avatars0.githubusercontent.com/u/1481077?s=60&v=4"
            width="30"
            height="30"
            alt="@gragland"
    />
    <a href="https://github.com/tjshipe"
    ><img
            src="https://avatars2.githubusercontent.com/u/1254942?s=60&v=4"
            width="30"
            height="30"
            alt="@tjshipe"
    />
    <a href="https://github.com/krnlde"
    ><img
            src="https://avatars1.githubusercontent.com/u/1087002?s=60&v=4"
            width="30"
            height="30"
            alt="@krnlde"
    />
    <a href="https://github.com/msutkowski"
    ><img
            src="https://avatars2.githubusercontent.com/u/784953?s=60&v=4"
            width="30"
            height="30"
            alt="@msutkowski"
    />
    <a href="https://github.com/mlukaszczyk"
    ><img
            src="https://avatars3.githubusercontent.com/u/599247?s=60&v=4"
            width="30"
            height="30"
            alt="@mlukaszczyk"
    />
    <a href="https://github.com/susshma"
    ><img
            src="https://avatars0.githubusercontent.com/u/2566818?s=460&u=754ee26b96e321ff28dbc4a2744132015f534fe0&v=4"
            width="30"
            height="30"
    />
    <a href="https://github.com/MatiasCiccone"
    ><img
            src="https://avatars3.githubusercontent.com/u/32602795?s=460&u=6a0c4dbe23c4f9a5628dc8867842b75989ecc4aa&v=4"
            width="30"
            height="30"
    />

## Backers

Thanks go to all our backers! [Become a backer].

## Organizations

Thanks go to these wonderful organizations! [Contribute].

## Contributors

Thanks go to these wonderful people! [Become a contributor].
