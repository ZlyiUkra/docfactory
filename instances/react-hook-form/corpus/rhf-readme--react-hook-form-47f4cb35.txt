# React Hook Form README 7.5.2-beta.0 … 7.5.3-beta.0
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/7e1af4da3254b21ad4877266b7f3a0c6cd224639/README.md
# отримано: 2026-09-26
# версія: 7.5.3-beta.0, 7.5.2, 7.5.2-beta.0

npm downloads
npm
npm
Discord

Version 7 | Version 6

## Features

- Built with performance and DX in mind
- Embraces native form validation
- Out of the box integration with UI libraries
- Small size and no dependencies
- Follows HTML standard for validation
- Support Yup, Zod, Superstruct, Joi, Vest, class-validator, io-ts, nope or custom

## Install

    npm install react-hook-form

## Links

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
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const onSubmit = (data) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('firstName')} /> {/* register an input */}
      <input {...register('lastName', { required: true })} />
      {errors.lastName && <p>Last name is required.</p>}
      <input {...register('age', { pattern: /\d+/ })} />
      {errors.age && <p>Please enter number for age.</p>}
      <input type="submit" />
    </form>
  );
}
```

## Sponsors

Thanks go to these kind and lovely sponsors (companies and individuals)!

    <a href="https://github.com/sayav"
    ><img
            src="https://avatars1.githubusercontent.com/u/42376060?s=60&v=4"
            width="45"
            height="45"
            alt="@sayav"
    />
    <a href="https://github.com/lemcii"
    ><img
            src="https://avatars1.githubusercontent.com/u/35668113?s=60&v=4"
            width="45"
            height="45"
            alt="@lemcii"
    />
    <a href="https://github.com/washingtonsoares"
    ><img
            src="https://avatars.githubusercontent.com/u/5726140?v=4"
            width="45"
            height="45"
            alt="@washingtonsoares"
    />
    <a href="https://github.com/lixunn"
    ><img
            src="https://avatars.githubusercontent.com/u/4017964?v=4"
            width="45"
            height="45"
            alt="@lixunn"
    />
    <a href="https://github.com/SamSamskies"
    ><img
            src="https://avatars2.githubusercontent.com/u/3655410?s=60&v=4"
            width="45"
            height="45"
            alt="@SamSamskies"
    />
    <a href="https://github.com/peaonunes"
    ><img
            src="https://avatars2.githubusercontent.com/u/3356720?s=60&v=4"
            width="45"
            height="45"
            alt="@peaonunes"
    />
    <a href="https://github.com/wilhelmeek"
    ><img
            src="https://avatars2.githubusercontent.com/u/609452?s=60&v=4"
            width="45"
            height="45"
            alt="@wilhelmeek"
    />
    <a href="https://github.com/iwarner"
    ><img
            src="https://avatars2.githubusercontent.com/u/279251?s=60&v=4"
            width="45"
            height="45"
            alt="@iwarner"
    />
    <a href="https://github.com/joejknowles"
    ><img
            src="https://avatars2.githubusercontent.com/u/10728145?s=60&v=4"
            width="45"
            height="45"
            alt="@joejknowles"
    />
    <a href="https://github.com/chris-gunawardena"
    ><img
            src="https://avatars0.githubusercontent.com/u/5763108?s=60&v=4"
            width="45"
            height="45"
            alt="@chris-gunawardena"
    />
    <a href="https://github.com/Tymek"
    ><img
            src="https://avatars1.githubusercontent.com/u/2625371?s=60&v=4"
            width="45"
            height="45"
            alt="@Tymek"
    />
    <a href="https://github.com/Luchanso"
    ><img
            src="https://avatars0.githubusercontent.com/u/2098777?s=60&v=4"
            width="45"
            height="45"
            alt="@Luchanso"
    />
    <a href="https://github.com/vcarel"
    ><img
            src="https://avatars1.githubusercontent.com/u/1541093?s=60&v=4"
            width="45"
            height="45"
            alt="@vcarel"
    />
    <a href="https://github.com/gragland"
    ><img
            src="https://avatars0.githubusercontent.com/u/1481077?s=60&v=4"
            width="45"
            height="45"
            alt="@gragland"
    />
    <a href="https://github.com/tjshipe"
    ><img
            src="https://avatars2.githubusercontent.com/u/1254942?s=60&v=4"
            width="45"
            height="45"
            alt="@tjshipe"
    />
    <a href="https://github.com/krnlde"
    ><img
            src="https://avatars1.githubusercontent.com/u/1087002?s=60&v=4"
            width="45"
            height="45"
            alt="@krnlde"
    />
    <a href="https://github.com/msutkowski"
    ><img
            src="https://avatars2.githubusercontent.com/u/784953?s=60&v=4"
            width="45"
            height="45"
            alt="@msutkowski"
    />
    <a href="https://github.com/mlukaszczyk"
    ><img
            src="https://avatars3.githubusercontent.com/u/599247?s=60&v=4"
            width="45"
            height="45"
            alt="@mlukaszczyk"
    />
    <a href="https://github.com/susshma"
    ><img
            src="https://avatars0.githubusercontent.com/u/2566818?s=460&u=754ee26b96e321ff28dbc4a2744132015f534fe0&v=4"
            width="45"
            height="45"
    />
    <a href="https://github.com/MatiasCiccone"
    ><img
            src="https://avatars3.githubusercontent.com/u/32602795?s=460&u=6a0c4dbe23c4f9a5628dc8867842b75989ecc4aa&v=4"
            width="45"
            height="45"
    />
    <a href="https://github.com/ghostwriternr"
    ><img
            src="https://avatars0.githubusercontent.com/u/10023615?s=460&u=3ec1e4ba991699762fd22a9d9ef47a0599f937dc&v=4"
            width="45"
            height="45"
    />
    <a href="https://github.com/neighborhood999"
    ><img
            src="https://avatars3.githubusercontent.com/u/10325111?s=450&u=f60c932f81d95a60f77f5c7f2eab4590e07c29af&v=4"
            width="45"
            height="45"
    />
    <a href="https://github.com/yjp20"
    ><img
            src="https://avatars3.githubusercontent.com/u/44457064?s=460&u=a55119c84e0167f6a3f830dbad3133b28f0c0a8f&v=4"
            width="45"
            height="45"
    />
    <a href="https://github.com/samantha-wong"
    ><img
            src="https://avatars.githubusercontent.com/u/19571028?s=460&u=7421a02f600646b5836d5973359a257950cae8c4&v=4"
            width="45"
            height="45"
    />
    <a href="https://github.com/msc-insure"
    ><img
            src="https://avatars.githubusercontent.com/u/44406870?s=200&v=4"
            width="45"
            height="45"
    />
    <a href="https://github.com/ccheney"
    ><img
            src="https://avatars.githubusercontent.com/u/302437?v=4"
            width="45"
            height="45"
    />
    <a href="https://github.com/artischockee"
    ><img
            src="https://avatars.githubusercontent.com/u/22125223?v=4"
            width="45"
            height="45"
    />

## Backers

Thanks go to all our backers! [Become a backer].

## Organizations

Thanks go to these wonderful organizations! [Contribute].

## Contributors

Thanks go to these wonderful people! [Become a contributor].
