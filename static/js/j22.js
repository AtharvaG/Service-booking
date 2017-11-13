// TODO: add mousewheel support to clock face

$.widget('wx.timepicker', {
  _create: function() {
    this.timepicker = $('<div class="timepicker"><div class="clock"><div class="unit hour bubble">Hr</div><div class="unit minute bubble">Min</div><div class="face"><div class="time-bubbles"></div><div class="minute hand"></div><div class="hour hand"></div></div><div class="meridiem am bubble">AM</div><div class="meridiem pm bubble">PM</div></div><div class="done">Done</div></div>').hide().insertAfter(this.element);
    this.hour = 0;
    this.minute = 0;
    this.meridiem = 0; // 0=am, 1=pm
    this.display = 0; // 0=none, 1=hours, 2=minutes
    this.isOpen = false;
    var self = this;
    
    this.element.prop('autocomplete',false);
    if(self._parseInput()) {
      self._refreshAll();
    }
    this.timepicker.find('.unit.minute').on('click', function() {
      self._buildMinutes();
    });
    this.timepicker.find('.unit.hour').on('click', function() {
      self._buildHours();
    });
    this.timepicker.on('click', '.time.hour', function() {
      self.hour = $(this).data('value');
      self._buildMinutes();
      self._refreshAll();
    });
    this.timepicker.on('click', '.time.minute', function() {
      self.minute = $(this).data('value');
      self._refreshAll();
    });
    this.element.on('focus click', function() {
      self._open();
    });
    this.timepicker.on('mousedown', function(e) {
      return false;
    });
    this.element.on('blur', function(e) {
      self._parseInput();
      self._refreshInput();
      self._close();
    });
    this.element.on('input', function() {
      if(self._parseInput()) {
        self._refreshClock();
      }
    });
    this.timepicker.find('.done').on('click', function() {
      self.element.focus();
      self._close();
    });
    this.timepicker.find('.meridiem.am').on('click', function() {
      self.meridiem = 0;
      self._refreshAll();
    });
    this.timepicker.find('.meridiem.pm').on('click', function() {
      self.meridiem = 1;
      self._refreshAll();
    });
  },
  
  _open: function() {
    if(!this.isOpen) {
      var offset = this.element.offset();
      this.timepicker.css({
        'left':offset.left+'px',
        'top':(offset.top+this.element.outerHeight())+'px'
      }).show();
      this.isOpen = true;
      this._buildHours();
    }
  },
  
  _close: function() {
    if(this.isOpen) {
      this.timepicker.hide();
      this.isOpen = false;
    }
  },
  
  _refreshAll: function() {
    this._refreshInput();
    this._refreshClock();
  },
  
  _refreshInput: function() {
    var hour = this.hour === 0 ? 12 : this.hour;
    var minute = this.minute < 10 ? '0'+this.minute : this.minute;
    this.element.val(hour+':'+minute+(this.meridiem?'pm':'am'));
  },
  
  _refreshClock: function() {
    var self = this;
    if(this.meridiem) {
      this.timepicker.find('.meridiem.am').removeClass('selected');
      this.timepicker.find('.meridiem.pm').addClass('selected');
    } else {
      this.timepicker.find('.meridiem.pm').removeClass('selected');
      this.timepicker.find('.meridiem.am').addClass('selected');
    }
    this.timepicker.find('.time.selected').removeClass('selected');
    if(this.display === 1) {
      this.timepicker.find('.time.hour').filter(function() {
        return $(this).data('value') === self.hour;
      }).addClass('selected');
    } else {
      this.timepicker.find('.time.minute').filter(function() {
        return $(this).data('value') === self.minute;
      }).addClass('selected');
    }
    this.timepicker.find('.hand.hour').css('transform', 'rotate(' + (this.hour / 12 * 360) + 'deg)');
    this.timepicker.find('.hand.minute').css('transform', 'rotate(' + (this.minute / 60 * 360) + 'deg)');
  },
  
  _parseInput: function() {
    var time = $.trim(this.element.val());
    var match;
    var valid = false;
    this.hour = 0;
    this.minute = 0;
    this.meridiem = 0;
    if(time.length > 0 && (match = /^(\d{1,2})(?::?(\d{2}))?(?: ?([ap])\.?(?:m\.?)?)?$/i.exec(time))) {
      valid = true;
      this.hour = parseInt(match[1]);
      this.minute = match[2] ? parseInt(match[2]) : 0;
      if(match[3] && match[3].toLowerCase() === 'p') {
        this.meridiem = 1;
      }
    }
    if(this.minute >= 60) {
      this.hour += Math.floor(this.minute/60);
      this.minute = this.minute % 60;
    }
    if(this.hour >= 12) {
      this.meridiem = 1;
      this.hour = this.hour % 12;
    }
    return valid;
  },
  
  _buildHours: function() {
    if(this.display === 1) return;
    this.display = 1;
    var r = this.timepicker.find('.face').width() / 2;
    var j = r - 22;
    var bubbles = [];
    for(var hour = 0; hour < 12; ++hour) {
      var x = j * Math.sin(Math.PI * 2 * (hour / 12));
      var y = j * Math.cos(Math.PI * 2 * (hour / 12));
      var bubble = $('<div>', {'class': 'time hour bubble'})
      .text(hour == 0 ? 12 : hour)
      .css({
        marginLeft: (x + r - 15) + 'px',
        marginTop: (-y + r - 15) + 'px'
      })
      .data('value', hour);
      if(this.hour === hour) bubble.addClass('selected');
      bubbles.push(bubble);
    }
    this.timepicker.find('.time-bubbles').html(bubbles);
    this.timepicker.find('.minute.hand').removeClass('selected');
    this.timepicker.find('.minute.unit').removeClass('selected');
    this.timepicker.find('.hour.hand').addClass('selected').appendTo(this.timepicker.find('.face'));
    this.timepicker.find('.hour.unit').addClass('selected');
  },
  
  _buildMinutes: function() {
    if(this.display === 2) return;
    this.display = 2;
    var r = this.timepicker.find('.face').width() / 2;
    var j = r - 22;
    var bubbles = [];
    for(var min = 0; min < 60; min += 5) {
      var str = min < 10 ? '0' + min : String(min);
      var x = j * Math.sin(Math.PI * 2 * (min / 60));
      var y = j * Math.cos(Math.PI * 2 * (min / 60));
      var bubble = $('<div>', {'class': 'time minute bubble'})
      .text(str)
      .css({
        marginLeft: (x + r - 15) + 'px',
        marginTop: (-y + r - 15) + 'px'
      })
      .data('value', min);
      if(this.minute === min) bubble.addClass('selected');
      bubbles.push(bubble);
    }
    this.timepicker.find('.time-bubbles').html(bubbles);
    this.timepicker.find('.hour.hand').removeClass('selected');
    this.timepicker.find('.hour.unit').removeClass('selected');
    this.timepicker.find('.minute.hand').addClass('selected').appendTo(this.timepicker.find('.face'));
    this.timepicker.find('.minute.unit').addClass('selected');
  }
});

$('#input').timepicker();