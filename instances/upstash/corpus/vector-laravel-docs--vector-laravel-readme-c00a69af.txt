# Upstash Vector SDK for Laravel
# джерело: https://github.com/upstash/vector-laravel/blob/v0.1.0/README.md
# отримано: 2026-10-16
# версія: vector-laravel-0.1.0

Latest Version on Packagist
GitHub Tests Action Status
GitHub Code Style Action Status
Total Downloads

Upstash Vector is an HTTP serverless Vector Database.

You can store, query, and retrieve vectors from your application, use it to power your search, and more.

You can read more about Upstash Vector here.

## Installation

You can install the package via composer:

```bash
composer require upstash/vector-laravel
```

You can publish the config file with:

```bash
php artisan vendor:publish --tag="vector-config"
```

This is the contents of the published config file:

```php
return [
    'default' => env('UPSTASH_VECTOR_CONNECTION', 'default'),

    'connections' => [
        'default' => [
            'url' => env('UPSTASH_VECTOR_REST_URL'),
            'token' => env('UPSTASH_VECTOR_REST_TOKEN'),
        ],
    ],
];
```

## Usage

```php
use Upstash\Vector\Laravel\Facades\Vector;

$info = Vector::getInfo();
```

## Testing

```bash
composer test
```

## Changelog

Please see CHANGELOG for more information on what has changed recently.

## Contributing

Please see CONTRIBUTING for details.

## Security Vulnerabilities

Please review our security policy on how to report security vulnerabilities.

## License

The MIT License (MIT). Please see License File for more information.
