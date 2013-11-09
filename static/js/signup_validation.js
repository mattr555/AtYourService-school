// Generated by CoffeeScript 1.6.3
(function() {
  jQuery(function() {
    $('input[name="username"]').on('keyup', function() {
      var t;
      t = this;
      if (this.value !== this.lastValue) {
        if (this.timer) {
          clearTimeout(this.timer);
        }
        $('#username-help').html('...');
        this.timer = setTimeout(function() {
          $.ajax({
            url: '/ajax/main/username_valid.json',
            type: 'POST',
            data: {
              username: t.value
            },
            success: function(j) {
              $('#username-help').html(j.data.message);
              if (j.data.valid === true) {
                $('#username-help').parent().addClass('has-success').removeClass('has-error');
              } else {
                $('#username-help').parent().addClass('has-error').removeClass('has-success');
              }
              return void 0;
            }
          });
          return void 0;
        });
        this.lastValue = this.value;
      }
      return void 0;
    });
    $('input[name="password2"]').on('keyup', function() {
      if (this.value !== $('input[name="password1"]')[0].value) {
        $('#password-help').html('Passwords do not match');
        return $('#password-help').parent().addClass('has-error').removeClass('has-success');
      } else {
        $('#password-help').html('');
        return $('#password-help').parent().addClass('has-success').removeClass('has-error');
      }
    });
    $('button[type="submit"]').on('click', function() {
      return void 0;
    });
    return void 0;
  });

}).call(this);