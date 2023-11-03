/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./*.{html,js}', './js/*.js'],
  theme: {
    extend: {
      colors: {
        'my-grey': '#aaaaaa',
      },
    },
  },
  plugins: [],
};
