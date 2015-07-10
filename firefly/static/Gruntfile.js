'use strict';

module.exports = function (grunt) {

    grunt.initConfig({
      react: {
        dynamic_mappings: {
          files: [
            {
              expand: true,
              cwd: 'javascripts/src/',
              src: ['*.jsx'],
              dest: 'javascripts',
              ext: '.js'
            }
          ]
        }
      },
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
        },
        react: {
          files: 'javascripts/src/*.jsx',
          tasks: ['react']
        }
      },
      sass_globbing: {
        sass: {
          files: {
            'stylesheets/scss/common.scss': 'stylesheets/scss/common/*.scss',
            'stylesheets/scss/topic.scss': 'stylesheets/scss/topic/*.scss',
            'stylesheets/scss/home.scss': 'stylesheets/scss/home/*.scss',
          },
          options: {
            useSingleQuoates: false
          }
        }
      },
      sass: {
        dev: {
          files: {
            'stylesheets/index.css': 'stylesheets/scss/index.scss',
            'stylesheets/post.css': 'stylesheets/scss/post.scss',
          }
        }
      }
    });

  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-sass-globbing');
  grunt.loadNpmTasks('grunt-react');

  grunt.registerTask('default', ['sass_globbing', 'sass', 'watch', 'react']);
};
