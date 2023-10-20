/** @type {import('tailwindcss').Config} */
const colors = require("tailwindcss/colors");
module.exports = {
    content: [
        "./src/**/*.{html,js}",
        "./node_modules/flowbite/**/*.js"
    ],
    theme: {
        colors: colors,
        extend: {},
    },
    plugins: [
        require('flowbite/plugin')
    ],
};
