require.config({
  baseUrl: '/static/javascripts/',
  paths: {
    'jquery': 'libs/jquery-2.1.3.min',
    'sweetAlert': 'libs/sweet-alert.min',
    'select2': 'libs/select2.min',
    'mousetrap': 'libs/mousetrap.min',
  },
  shim: {
  }
});

require(['login', 'keyboard'], function(Login, Keyboard){
  var login = Login();
  Keyboard(login);
});
