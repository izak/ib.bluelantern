#!/bin/sh
mkdir -p build
cat \
    app/bower_components/html5-boilerplate/dist/js/vendor/modernizr-2.8.3.min.js \
    app/bower_components/angular/angular.js \
    app/bower_components/angular-route/angular-route.js \
    app/bower_components/raphael/raphael.js \
    app/bower_components/justgage-bower/justgage.js \
    app/bower_components/angular-gage/dist/angular-gage.js \
    | node_modules/uglify-js/bin/uglifyjs -mc > app/build/bower-libs.js
