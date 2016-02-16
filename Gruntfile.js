module.exports = function(grunt) {
    'use strict';
    var DEBUG = grunt.option('debug');

    grunt.initConfig({
        browserify: {
            app: {
                files: {
                    'client/dist/js/main.js': 'client/src/js/main.js'
                }
            }
        },

        jshint: {
            options: {
                node: true,
                browser: true,
                unused: true
            },
            js: {
                src: [
                    'client/src/js/**/*.js',
                    'client/src/js/*.js'
                ]
            }
        },

        nunjucks: {
            app: {
                baseDir: 'client/src/templates/',
                src: 'client/src/templates/*',
                dest: 'client/build/templates.js',
            }
        },

        copy: {
            images: {
                files: [
                    {
                        expand: true,
                        cwd: 'client/src/img/',
                        src: '**',
                        dest: 'client/dist/img/'
                    }
                ],
            },
        },

        sass: {
            options: {
                sourceMap: true,
                outputStyle: (DEBUG ? 'nested' : 'compressed')
            },
            dist: {
                files: [
                    {
                        expand: true,
                        cwd: 'client/src/sass/',
                        src: ['[^_]*.scss'],
                        dest: 'client/dist/css/',
                        ext: '.css',
                    }
                ]
            }
        },

        uglify: {
            options: {
                mangle: !DEBUG,
                compress: !DEBUG,
                beautify: DEBUG,
                report: 'gzip',
            },
            app: {
                files: {
                    'client/dist/js/main.js': [
                        'client/build/templates.js',
                        'client/dist/js/main.js'
                    ]
                }
            }
        },

        watch: {
            options: {
                spawn: false,
                interrupt: true,
            },

            configFiles: {
                files: ['Gruntfile.js'],
                options: {
                    reload: true
                }
            },

            js: {
                files: ['client/src/**/*.js', 'client/src/**/*.html'],
                tasks: ['js'],
                options: {
                    reload: true
                }
            },

            sass: {
                files: ['client/src/sass/*.scss', 'client/src/sass/*.sass'],
                tasks: ['css']
            }
        }
    });

    grunt.loadNpmTasks('grunt-browserify');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-nunjucks');
    grunt.loadNpmTasks('grunt-sass');

    grunt.registerTask('css', ['copy', 'sass']);
    grunt.registerTask('js', ['jshint', 'nunjucks', 'browserify', 'uglify']);

    grunt.registerTask('build', ['css', 'js']);
    grunt.registerTask('default', ['build', 'watch']);
};
