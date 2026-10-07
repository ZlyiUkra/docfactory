# React Hook Form README 6.12.0 … 6.15.8
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/cffed3ae9adaf2b756c9adebbbd93a23ab13caaa/README.md
# отримано: 2026-09-26
# версія: 6.15.8, 6.15.7, 6.15.6, 6.15.5, 6.15.5-beta.0, 6.15.4, 6.15.3, 6.15.2, 6.15.2-beta.3, 6.15.2-beta.2, 6.15.2-beta.1, 6.15.1, 6.15.0, 6.14.2, 6.14.1, 6.14.0, 6.13.1, 6.13.0, 6.12.3-beta.2, 6.12.3-beta.1, 6.12.2, 6.12.2-beta.1, 6.12.1, 6.12.1-beta.2, 6.12.1-beta.1, 6.12.0

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
- Resolvers support Yup, Zod, Superstruct, Joi or custom
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
            width="40"
            height="40"
            alt="@sayav"
    />
    <a href="https://github.com/lemcii"
    ><img
            src="https://avatars1.githubusercontent.com/u/35668113?s=60&v=4"
            width="40"
            height="40"
            alt="@lemcii"
    />
    <a href="https://github.com/washingtonsoares"
    ><img
            src="https://avatars0.githubusercontent.com/u/5726140?s=460&u=b300a6fa08a24c59b9db6ebf246384cf8b16a140&v=4"
            width="40"
            height="40"
            alt="@washingtonsoares"
    />
    <a href="https://github.com/lixunn"
    ><img
            src="https://avatars0.githubusercontent.com/u/4017964?s=460&u=3a3fdffeb97749d7509d9c5e9be2cafcb98e426f&v=4"
            width="40"
            height="40"
            alt="@lixunn"
    />
    <a href="https://github.com/SamSamskies"
    ><img
            src="https://avatars2.githubusercontent.com/u/3655410?s=60&v=4"
            width="40"
            height="40"
            alt="@SamSamskies"
    />
    <a href="https://github.com/peaonunes"
    ><img
            src="https://avatars2.githubusercontent.com/u/3356720?s=60&v=4"
            width="40"
            height="40"
            alt="@peaonunes"
    />
    <a href="https://github.com/wilhelmeek"
    ><img
            src="https://avatars2.githubusercontent.com/u/609452?s=60&v=4"
            width="40"
            height="40"
            alt="@wilhelmeek"
    />
    <a href="https://github.com/iwarner"
    ><img
            src="https://avatars2.githubusercontent.com/u/279251?s=60&v=4"
            width="40"
            height="40"
            alt="@iwarner"
    />
    <a href="https://github.com/joejknowles"
    ><img
            src="https://avatars2.githubusercontent.com/u/10728145?s=60&v=4"
            width="40"
            height="40"
            alt="@joejknowles"
    />
    <a href="https://github.com/chris-gunawardena"
    ><img
            src="https://avatars0.githubusercontent.com/u/5763108?s=60&v=4"
            width="40"
            height="40"
            alt="@chris-gunawardena"
    />
    <a href="https://github.com/Tymek"
    ><img
            src="https://avatars1.githubusercontent.com/u/2625371?s=60&v=4"
            width="40"
            height="40"
            alt="@Tymek"
    />
    <a href="https://github.com/Luchanso"
    ><img
            src="https://avatars0.githubusercontent.com/u/2098777?s=60&v=4"
            width="40"
            height="40"
            alt="@Luchanso"
    />
    <a href="https://github.com/vcarel"
    ><img
            src="https://avatars1.githubusercontent.com/u/1541093?s=60&v=4"
            width="40"
            height="40"
            alt="@vcarel"
    />
    <a href="https://github.com/gragland"
    ><img
            src="https://avatars0.githubusercontent.com/u/1481077?s=60&v=4"
            width="40"
            height="40"
            alt="@gragland"
    />
    <a href="https://github.com/tjshipe"
    ><img
            src="https://avatars2.githubusercontent.com/u/1254942?s=60&v=4"
            width="40"
            height="40"
            alt="@tjshipe"
    />
    <a href="https://github.com/krnlde"
    ><img
            src="https://avatars1.githubusercontent.com/u/1087002?s=60&v=4"
            width="40"
            height="40"
            alt="@krnlde"
    />
    <a href="https://github.com/msutkowski"
    ><img
            src="https://avatars2.githubusercontent.com/u/784953?s=60&v=4"
            width="40"
            height="40"
            alt="@msutkowski"
    />
    <a href="https://github.com/mlukaszczyk"
    ><img
            src="https://avatars3.githubusercontent.com/u/599247?s=60&v=4"
            width="40"
            height="40"
            alt="@mlukaszczyk"
    />
    <a href="https://github.com/susshma"
    ><img
            src="https://avatars0.githubusercontent.com/u/2566818?s=460&u=754ee26b96e321ff28dbc4a2744132015f534fe0&v=4"
            width="40"
            height="40"
    />
    <a href="https://github.com/MatiasCiccone"
    ><img
            src="https://avatars3.githubusercontent.com/u/32602795?s=460&u=6a0c4dbe23c4f9a5628dc8867842b75989ecc4aa&v=4"
            width="40"
            height="40"
    />
    <a href="https://github.com/ghostwriternr"
    ><img
            src="https://avatars0.githubusercontent.com/u/10023615?s=460&u=3ec1e4ba991699762fd22a9d9ef47a0599f937dc&v=4"
            width="40"
            height="40"
    />
    <a href="https://github.com/neighborhood999"
    ><img
            src="https://avatars3.githubusercontent.com/u/10325111?s=400&u=f60c932f81d95a60f77f5c7f2eab4590e07c29af&v=4"
            width="40"
            height="40"
    />
    <a href="https://github.com/yjp20"
    ><img
            src="https://avatars3.githubusercontent.com/u/44457064?s=460&u=a55119c84e0167f6a3f830dbad3133b28f0c0a8f&v=4"
            width="40"
            height="40"
    />

## Backers

Thanks go to all our backers! [Become a backer].

## Organizations

Thanks go to these wonderful organizations! [Contribute].

## Contributors

Thanks go to these wonderful people! [Become a contributor].
