/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./src/templates/**/*.{html,js}"],
    theme: {
        fontFamily: {
            sans: [
                "Poppins",
                "Helvetica",
                "Arial",
                "ui-sans-serif",
                "system-ui",
            ],
        },
        extend: {},
    },
    plugins: [],
};
