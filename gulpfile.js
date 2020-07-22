var gulp = require('gulp');
var sass = require('gulp-sass');
var minify = require('gulp-minify');
var cleanCSS = require('gulp-clean-css');
var concat = require('gulp-concat');
var del = require('del');


const compile_sass = () => {
    return gulp.src(['public/scss/*.scss', 'public/scss/**/*.scss'])
        .pipe(sass({ outputStyle: 'compressed' }))
        .pipe(gulp.dest('public/gulp/css'));
}


const minify_css = () => {
    return gulp.src('public/gulp/css/*.css')
        .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(gulp.dest('public/gulp/css/minify'));
}


const minify_js = () => {
    return gulp.src(['public/js/*.js', 'public/js/**/*.js'])
        .pipe(minify({
            ext: {
                min: '.min.js'
            },
            ignoreFiles: ['-min.js']
        }))
        .pipe(gulp.dest('public/gulp/js'))
}


const concat_js = () => {
    return gulp.src(['public/gulp/js/*.min.js', 'public/gulp/js/**/*.min.js'])
        .pipe(concat('all.min.js'))
        .pipe(gulp.dest('public/gulp/js/minify'))
}


const clean = () => {
    return del('public/gulp', {force:true});
}


gulp.task('compile-sass', compile_sass);

gulp.task('minify-css', minify_css);

gulp.task('minify-js', minify_js);

gulp.task('concat-js', concat_js);

gulp.task('clean', clean);


gulp.task('default', gulp.series(
    clean, compile_sass,  minify_css, minify_js, concat_js
));