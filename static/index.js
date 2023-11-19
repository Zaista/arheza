/* global $ */

$(async function () {
    'use strict';
    
    let imageRequested = false

    $('#background').on('generateImage', (event, imagePrompt) => {
        
        if (imageRequested === false) {
            $.ajax('/image', {
                type: 'POST',
                data: JSON.stringify({prompt: imagePrompt}),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                success: function (result) {
                    const backgroundImage = new Image();
                    backgroundImage.onload = function () {
                        console.log("image is loaded");
                        $('#background').css('background-image', `url(${result.url})`);
                    }
                    backgroundImage.src = result.url;
                }
            });
            imageRequested = true;
        } else {
            console.log('woooopsie')
        }
    })

    $('#button').on('click', function () {
        $('#start').prop('hidden', true);
        $('#description').prop('hidden', false);

        const eventSource = new EventSource('/story');
        let imageFlag = true;
        let imagePrompt = '';

        // Handle incoming chunks
        eventSource.onmessage = function (event) {
            if (imagePrompt.includes('end-of-image-prompt')) {
                imagePrompt = imagePrompt.replace('end-of-image-prompt', ''); // TODO this can cause infinite images
                imageFlag = false;
                $('#background').trigger('generateImage', imagePrompt);
                return;
            }
            
            if (imageFlag) {
                imagePrompt += event.data
            } else {
                $('#text').append(event.data);
            }
        };

        // Handle connection closure
        eventSource.onerror = function () {
            eventSource.close();
        };
    });
});