# React Hook Form README 7.32.1 … 7.32.2
# джерело: https://raw.githubusercontent.com/react-hook-form/react-hook-form/461302ccef7ff7cf3a99700bb2699977f9f0638f/README.md
# отримано: 2026-09-26
# версія: 7.32.2, 7.32.1

https://user-images.githubusercontent.com/10513364/152621466-59a41c65-52b4-4518-9d79-ffa3fafa498a.mp4

npm downloads
npm
npm
Discord

  Get started |
  API |
  Examples |
  Demo |
  Form Builder |
  FAQs

### Features

- Built with performance, UX and DX in mind
- Embraces native HTML form validation
- Out of the box integration with UI libraries
- Small size and no dependencies
- Support Yup, Zod, AJV, Superstruct, Joi, Vest, class-validator, io-ts, nope and custom build

### Install

    npm install react-hook-form

### Quickstart

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
      <input {...register('firstName')} />
      <input {...register('lastName', { required: true })} />
      {errors.lastName && <p>Last name is required.</p>}
      <input {...register('age', { pattern: /\d+/ })} />
      {errors.age && <p>Please enter number for age.</p>}
      <input type="submit" />
    </form>
  );
}
```

### Sponsors

Thanks go to these kind and lovely sponsors (companies and individuals)!

    <img
      src="https://avatars1.githubusercontent.com/u/42376060?s=60&v=4"
      width="45"
      height="45"
      alt="@sayav"
    />

    <img
      src="https://avatars1.githubusercontent.com/u/35668113?s=60&v=4"
      width="45"
      height="45"
      alt="@lemcii"
    />

    <img
      src="https://avatars.githubusercontent.com/u/5726140?v=4"
      width="45"
      height="45"
      alt="@washingtonsoares"
    />

    <img
      src="https://avatars.githubusercontent.com/u/4017964?v=4"
      width="45"
      height="45"
      alt="@lixunn"
    />

    <img
      src="https://avatars2.githubusercontent.com/u/3655410?s=60&v=4"
      width="45"
      height="45"
      alt="@SamSamskies"
    />

    <img
      src="https://avatars2.githubusercontent.com/u/3356720?s=60&v=4"
      width="45"
      height="45"
      alt="@peaonunes"
    />

    <img
      src="https://avatars2.githubusercontent.com/u/609452?s=60&v=4"
      width="45"
      height="45"
      alt="@wilhelmeek"
    />

    <img
      src="https://avatars2.githubusercontent.com/u/279251?s=60&v=4"
      width="45"
      height="45"
      alt="@iwarner"
    />

    <img
      src="https://avatars2.githubusercontent.com/u/10728145?s=60&v=4"
      width="45"
      height="45"
      alt="@joejknowles"
    />

    <img
      src="https://avatars0.githubusercontent.com/u/5763108?s=60&v=4"
      width="45"
      height="45"
      alt="@chris-gunawardena"
    />

    <img
      src="https://avatars1.githubusercontent.com/u/2625371?s=60&v=4"
      width="45"
      height="45"
      alt="@Tymek"
    />

    <img
      src="https://avatars0.githubusercontent.com/u/2098777?s=60&v=4"
      width="45"
      height="45"
      alt="@Luchanso"
    />

    <img
      src="https://avatars1.githubusercontent.com/u/1541093?s=60&v=4"
      width="45"
      height="45"
      alt="@vcarel"
    />

    <img
      src="https://avatars0.githubusercontent.com/u/1481077?s=60&v=4"
      width="45"
      height="45"
      alt="@gragland"
    />

    <img
      src="https://avatars2.githubusercontent.com/u/1254942?s=60&v=4"
      width="45"
      height="45"
      alt="@tjshipe"
    />

    <img
      src="https://avatars1.githubusercontent.com/u/1087002?s=60&v=4"
      width="45"
      height="45"
      alt="@krnlde"
    />

    <img
      src="https://avatars2.githubusercontent.com/u/784953?s=60&v=4"
      width="45"
      height="45"
      alt="@msutkowski"
    />

    <img
      src="https://avatars3.githubusercontent.com/u/599247?s=60&v=4"
      width="45"
      height="45"
      alt="@mlukaszczyk"
    />

    <img
      src="https://avatars0.githubusercontent.com/u/2566818?s=460&u=754ee26b96e321ff28dbc4a2744132015f534fe0&v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars3.githubusercontent.com/u/32602795?s=460&u=6a0c4dbe23c4f9a5628dc8867842b75989ecc4aa&v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars0.githubusercontent.com/u/10023615?s=460&u=3ec1e4ba991699762fd22a9d9ef47a0599f937dc&v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars3.githubusercontent.com/u/10325111?s=450&u=f60c932f81d95a60f77f5c7f2eab4590e07c29af&v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars3.githubusercontent.com/u/44457064?s=460&u=a55119c84e0167f6a3f830dbad3133b28f0c0a8f&v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/19571028?s=460&u=7421a02f600646b5836d5973359a257950cae8c4&v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/44406870?s=200&v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/302437?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/22125223?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/2079598?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/2396344?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/1953965?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/41862257?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/43356139?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/1137112?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/2914170?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/45594821?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/5769153?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/12868063?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/459267?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/1941348?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/12888685?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/22803185?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/36793907?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/40028548?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/16930958?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/2019893?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/5480441?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/28400709?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/41503068?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/699616?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/47701145?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/4616705?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/10516382?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/548371?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/42692074?v=4"
      width="45"
      height="45"
    />

    <img
      src="https://avatars.githubusercontent.com/u/34721312?v=4"
      width="45"
      height="45"
    />

### Backers

Thanks go to all our backers! [Become a backer].

### Contributors

Thanks go to these wonderful people! [Become a contributor].

### Helpers

Thank you for helping and answering questions from the community.

### Organizations

Thanks go to these wonderful organizations! [Contribute].
