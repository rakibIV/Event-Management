/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
    './static/**/*.css',
  ],
  theme: {
    extend: {
      height: {
        'custom-24': '24rem',
      },
    },
  },
  plugins: [],
}

