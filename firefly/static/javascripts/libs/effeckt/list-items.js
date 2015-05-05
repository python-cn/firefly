define(['jquery'], function($) {
  function EffecktListItems() {
    if (!(this instanceof EffecktListItems)) {
      return new EffecktListItems();
    }
    this._init();
  }

  EffecktListItems.prototype = {
    constructor: EffecktListItems,
    _init: function() {

      // List of all animation/transition properties
      // with its animationEnd/transitionEnd event
      this.animationEndEventNames = {
        'WebkitAnimation' : 'webkitAnimationEnd',
        'OAnimation' : 'oAnimationEnd',
        'msAnimation' : 'MSAnimationEnd',
        'animation' : 'animationend'
      };

      this.transitionEndEventNames = {
        'WebkitTransition' : 'webkitTransitionEnd',
        'OTransition' : 'oTransitionEnd',
        'msTransition' : 'MSTransitionEnd',
        'transition' : 'transitionend'
      };
      this.transitionAnimationEndEvent = this.getTransitionEndEventNames + '' + this.getAnimationEndEventNames();
    },
    // Get all the properties for transition/animation end
    getTransitionEndEventNames: function() {
      return this._getEndEventNames( this.transitionEndEventNames );
    },

    getAnimationEndEventNames: function() {
      return this._getEndEventNames( this.animationEndEventNames );
    },

    _getEndEventNames: function(obj) {
      var events = [];

      for ( var eventName in obj ) {
        events.push( obj[ eventName ] );
      }

      return events.join(' ');
    },

    addListItem: function(insertData, insertPoint) {
      $(insertData).insertBefore(insertPoint);
    },

    removeListItem: function(el) {
      var $parent = $(el).parent(),
          self = this;

      var elToRemove = $parent.find("li.new-item").last();
      elToRemove.on( this.transitionAnimationEndEvent, function () {
        elToRemove.off( this.transitionAnimationEndEvent );
        elToRemove.remove();
      });

      elToRemove.toggleClass("remove-item new-item");
      if (!$parent.find("li.new-item").length) {
        $parent.find("button.remove").hide();
      }
    }
  };

  return EffecktListItems;
});
