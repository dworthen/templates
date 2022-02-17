# Templates

Project templates to be scaffolded out by [degit](https://www.npmjs.com/package/degit).

```
$ npm install degit -g
$ degit dworthen/templates#BRANCH_NAME PROJECT_NAME
```

Every branch in this repo is a different project template. 

Here is an example of scaffolding out a [pnpm](https://pnpm.io/) monorepo structure containing a react-vite application.

```
$ degit dworthen/templates#monorepo-pnpm my-project
$ cd my-project/packages
$ degit dworthen/templates#react-vite webapp
```