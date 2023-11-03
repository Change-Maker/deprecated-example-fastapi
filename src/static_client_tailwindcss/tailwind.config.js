/** @type {import('tailwindcss').Config} */
export default {
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
