/** @type {import('vercel').VercelConfig} */
const config = {
  version: 2,
  builds: [
    {
      src: "package.json",
      use: "@vercel/static-build",
      config: {
        distDir: "build", // Docusaurus build folder
      },
    },
  ],
  routes: [
    { src: "/(.*)", dest: "/index.html" }, // SPA routing
  ],
  env: {
    NODE_VERSION: "24", // Match your package.json engines
  },
};

module.exports = config;