var gulp = require('gulp');
var sass = require('gulp-sass');
var cleanCSS = require('gulp-clean-css');

var less = require('gulp-less');
var tap = require('gulp-tap');
var postcss = require('gulp-postcss');
var autoprefixer = require('autoprefixer');


gulp.task('build:sass', function() {
  //noinspection JSUnresolvedFunction
  gulp.src('static/css/*.scss')
    .pipe(sass({
      includePaths: ['./static/css', './static/bootstrap/css'],
      outputStyle: 'compact'
    }).on('error', sass.logError))
    .pipe(cleanCSS())
    .pipe(gulp.dest('./static/css/'));
});


gulp.task('default', function() {
  gulp.watch(['static/css/*.scss'], ['build:sass']);
});

