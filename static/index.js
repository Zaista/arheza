/* global $ */

$(async function() {
  'use strict';

  $('#promptButton').on('click', function() {
    $('#promptButton').prop('disabled', true);
    $('#loadingSpinner').prop('hidden', false);
//    $.post('/story', {}, function(result) {
//      $('#promptOutput').text(result);
      const eventSource = new EventSource('/story');

      // Handle incoming chunks
      eventSource.onmessage = function(event) {
          console.log('jebla')
          $('#promptOutput').append(event.data);
      };

      // Handle connection closure
      eventSource.onerror = function() {
        console.log('teeest')
          eventSource.close();
      };

      const result = '';

      $.post('/image', { prompt: result }, function(response) {
        $('#promptImage').prop('src', response);
        $('#promptImage').prop('hidden', false);
        $('#promptButton').prop('disabled', false);
        $('#loadingSpinner').prop('hidden', true);
      });
//    });
  });
});