var gulp = require('gulp');
var sass = require('gulp-sass');
var sassGlob = require('gulp-sass-glob');
var postcss      = require('gulp-postcss');
var autoprefixer = require('autoprefixer');
var cssvariables = require('postcss-css-variables');
var calc = require('postcss-calc');
var concat = require('gulp-concat');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');

// js file paths
var utilJsPath = 'src/js'; // util.js path - you may need to update this if including the framework as external node module
var componentsJsPath = 'src/js/components/*.js'; // component js files
var scriptsJsPath = 'public/js'; //folder for final scripts.js/scripts.min.js files

// css file paths
var cssFolder = 'public/css'; // folder for final style.css/style-custom-prop-fallbac.css files
var scssFilesPath = 'src/scss/**/*.scss'; // scss files to watch


gulp.task('sass', function() {
  return gulp.src(scssFilesPath)
  .pipe(sassGlob())
  .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
  .pipe(postcss([autoprefixer()]))
  .pipe(gulp.dest(cssFolder))
  .pipe(rename('style-fallback.css'))
  .pipe(postcss([cssvariables(), calc()]))
  .pipe(gulp.dest(cssFolder));
});

gulp.task('scripts', function() {
  return gulp.src([utilJsPath+'/util.js', componentsJsPath])
  .pipe(concat('scripts.js'))
  .pipe(gulp.dest(scriptsJsPath))
  .pipe(rename('scripts.min.js'))
  .pipe(uglify())
  .pipe(gulp.dest(scriptsJsPath))
});


gulp.task('watch', gulp.series(['sass', 'scripts'], function () {
  gulp.watch(scssFilesPath, gulp.series(['sass']));
  gulp.watch(componentsJsPath, gulp.series(['scripts']));
}));

gulp.task('default', gulp.series(['sass', 'scripts']));
