# Upstash Search Strapi Plugin
# джерело: https://github.com/upstash/strapi-plugin-upstash-search/blob/d991af3d346f0d070e9d18891423032c6f47876d/README.md
# отримано: 2026-10-16

⚡ The Upstash Search plugin for Strapi

Upstash Search is a **simple, lightweight, and scalable way to add AI-powered search to your app**.We combine full-text and semantic search for highly relevant results. Search works out of the box and scales to massive data sizes with zero infrastructure to manage.

## 📖 Documentation

To understand Upstash Search and how it works, see the Upstash Search documentation.

To understand Strapi and how to create an app, see Strapi's documentation.

## 🔧 Installation

This package works with Strapi v5.

Inside your Strapi app, add the package:

With `npm`:

```bash

npm  install  @upstash/strapi-plugin-upstash-search

```

With `yarn`:

```bash

yarn  add  @upstash/strapi-plugin-upstash-search

```

### 🔧 Create Upstash Search Database

Before using the plugin, you need to create an Upstash Search database:

1. Go to the Upstash Console

2. Navigate to the **Search** section

3. Click **Create Database**

4. Choose your region and configuration

5. Once created, copy your **REST URL** and **REST Token** from the database details

## 🚀 Getting started

Now that you have installed the plugin and have a running Strapi app, let's go to the plugin page on your admin dashboard.

On the left-navbar, `Upstash Search` appears under the `PLUGINS` category. If it does not, ensure that you have installed the plugin and re-build Strapi.

### 🤫 Add Credentials

First, you need to configure credentials via the plugin page. The credentials are composed of:

- **URL**: Your Upstash Search REST URL (e.g., `https://xxx-xxx-search.upstash.io`)

- **Token**: Your Upstash Search REST Token

1. In your Strapi admin panel, navigate to **Upstash Search** in the plugins section

2. Click on the **Credentials** tab

3. Enter your **URL** (found in your Upstash console under REST URL)

4. Enter your **Token** (found in your Upstash console under REST Token)

5. Click **Save Credentials**

You can find these credentials in your Upstash console Search tab. The plugin interface includes a direct link to the Upstash Search documentation for reference.

### 🚛 Add your content-types to Upstash Search

If you don't have any content-types yet in your Strapi project, please follow Strapi quickstart.

#### Collections Tab

1. Navigate to the **Collections** tab in the Upstash Search plugin

2. You'll see all your available content-types displayed as cards with:

- Content-type name (e.g., `restaurant`, `category`, `user`)

- Number of entries

- Current indexing status

- A toggle switch to enable/disable indexing

#### Adding Content-Types to Search

To index a content-type:

1.  **Click the toggle switch** next to a content-type to enable indexing

2.  A **configuration modal** will open where you can:

- **Select searchable fields**: Choose which fields should be searchable (required)

- **Set custom index name**: Specify a custom index name

3.  **Click confirm** to start indexing

The plugin will show a progress indicator while indexing is in progress. Once complete, your content will be searchable in Upstash Search.

### 🪝 Apply Hooks

Hooks are listeners that update Upstash Search each time you add/update/delete an entry in your content-types. They are automatically activated as soon as you enable indexing for a content-type.

#### Removing Content-Types

To remove a content-type from Upstash Search:

1.  **Toggle off** the switch next to the content-type

2.  The plugin will remove the content-type from indexing

The plugin interface will reload the server when needed.

## 💅 Customization

The Upstash Search plugin provides a simple UI-based configuration approach. All customization is done through the admin interface without requiring configuration files.

### 🏷 Custom Index Names

When configuring a content-type for indexing, you can specify a custom index name in the configuration modal:

- **Default behavior**: The plugin uses the content-type name as the index name by default

- **Custom naming**: Enter any name you prefer (e.g., `my_restaurants` instead of `restaurant`)

- **Shared indexes**: Multiple content-types can use the same index name to group them together

### 🔍 Searchable Fields Selection

The configuration modal allows you to choose exactly which fields should be searchable:

- **Required step**: You must select at least one field to enable indexing

- **Field types**: All field types from your content-type schema are available

- **Searchable vs Metadata**: Selected fields become searchable, while unselected fields are stored as metadata

### 🔄 Real-time Updates

The plugin automatically:

- Adds new entries to Upstash Search when created

- Updates existing entries when modified

- Removes entries from Upstash Search when deleted

### 🏗 Index Management

Through the admin interface, you can:

- Create and delete indexes

- Monitor indexing progress

- View index statistics

- Rebuild indexes when needed

## 🤖 Compatibility with Upstash Search and Strapi

**Supported Strapi versions**:

- Strapi `>=v5.x.x`

**Supported Node.js versions**:

- Node.js >= 18

**We recommend always using the latest version of Strapi to start your new projects**.

## ⚙️ Development Workflow and Contributing

Any new contribution is more than welcome in this project!

If you want to know more about the development workflow or want to contribute, please visit our contributing guidelines for detailed instructions!

## 🌎 Community support

- For general help using **Upstash Search**, please refer to the official Upstash documentation.

- For general help using **Strapi**, please refer to the official Strapi documentation.

- Contact Upstash support for Upstash-specific issues

- Join the Strapi community Slack for general Strapi help

## Features

- ✅ **UI-based Configuration**: No configuration files required - set everything up through the admin interface

- ✅ **Real-time Synchronization**: Automatic sync between Strapi and Upstash Search

- ✅ **Custom Index Names**: Configure custom index names for better organization

- ✅ **Searchable Field Selection**: Choose which fields to make searchable

- ✅ **Draft/Published Handling**: Proper handling of content states

- ✅ **Batch Operations**: Efficient batch processing for large datasets

- ✅ **Index Management**: Create, delete, and monitor indexes through the UI

- ✅ **Error Handling**: Comprehensive error handling and logging

- ✅ **Multi-index Support**: Support for multiple indexes per content-type

## Getting Help

If you encounter any issues or have questions:

1. Check the Upstash documentation

2. Review the Strapi documentation

3. Search existing GitHub issues

4. Create a new issue with detailed information about your problem
