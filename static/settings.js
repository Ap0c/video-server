// ----- Functions ----- //

// Sends a request to scan the media directories.
function scanMedia () {

	fetch('/scan', {method: 'post'}).then(function (response) {

		if (response.status !== 202) {
			var errorMessage = document.getElementById('error-message');
			errorMessage.textContent = 'Scan failed.';
		}

	});

}

// Sets up the event listeners on page buttons.
function setup () {

	var scanButton = document.getElementById('scan-button');
	var addMediaButton = document.getElementById('add-media-button');

	scanButton.addEventListener('click', scanMedia);

}


// ----- DOM Loaded ----- //

document.addEventListener('DOMContentLoaded', setup);
