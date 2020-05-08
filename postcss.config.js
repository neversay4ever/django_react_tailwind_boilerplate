// const purgeCSS = require('@fullhuman/postcss-purgecss');

// module.exports = {
//     plugins: [
//         require('tailwindcss'),
//         purgeCSS({
//             content: [
//                 './src/**/*.js',
//             ],
//             css: ['./src/**/*.css']
//         })
//     ]
// }


const tailwindcss = require('tailwindcss');
module.exports = {
    plugins: [
        tailwindcss('./tailwind.js'),
        require('autoprefixer')
    ],
};