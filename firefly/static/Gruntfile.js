'use strict';

module.exports = function (grunt) {

    grunt.initConfig({
        //    autoprefixer: {
        //      dist: {
        //        files: {
        //          'stylesheets/style.css': 'stylesheets/_style.css'
        //        }
        //      }
        //    },
        watch: {
            sass: {
                files: "stylesheets/scss/{,*/}*.scss",
                tasks: ["sass_globbing", "sass"]
            },
            css: {
                files: 'stylesheets/*.css',
                options: {
                    livereload: true
                }
            },
            html: {
                files: '../templates/**/*.html',
                options: {
                    livereload: true
                }
            }
        },
        sass_globbing: {
            sass: {
                files: {
                    'stylesheets/scss/common.scss': 'stylesheets/scss/common/*.scss',
                },
                options: {
                    useSingleQuoates: false
                }
            }
        },
        sass: {
            dev: {
                files: {
                    'stylesheets/style.css': 'stylesheets/scss/main.scss'
                }
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-sass-globbing');
    //    grunt.loadNpmTasks('grunt-autoprefixer');

    grunt.registerTask('default', ['sass_globbing', 'sass', 'watch']);
};
