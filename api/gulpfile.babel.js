import gulp from 'gulp';
import nodemon from 'gulp-nodemon';
import notify from 'gulp-notify';

gulp.task('start', () => {
    nodemon({
        script: 'server.js',
        ext: 'js', 
        env: {'NODE_ENV': 'develepment'}
    });
    // .on('restart', () => {
    //     gulp.src('server.js')
    //     .pipe(notify('Reloading page, please wait...'));
    // });
});

gulp.task('default', ['start']);