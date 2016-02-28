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

// Sends request to add source via fetch.
function addSource (form) {

	form.preventDefault();

	var data = new FormData(form.target);

	fetch('/add_source', { method: 'put', body: data })
		.then(function (response) {

			if (response.status === 201) {
				location.reload();
			} else {
				response.text().then(function (body) {
					var errorMessage = document.getElementById('error-message');
					errorMessage.textContent = body;
				});
			}

		});

}

// Sets up the event listeners on page buttons.
function setup () {

	var scanButton = document.getElementById('scan-button');
	scanButton.addEventListener('click', scanMedia);

	var sourceDialog = document.getElementById('add-media-dialog');
	dialogPolyfill.registerDialog(sourceDialog);

	var addMediaButton = document.getElementById('add-media-button');
	var closeDialogButton = document.getElementById('close-dialog-button');

	addMediaButton.addEventListener('click', function () {
		sourceDialog.showModal();
	});
	
	closeDialogButton.addEventListener('click', function () {
		sourceDialog.close();
	});

	var sourceForm = document.getElementById('source-form');
	sourceForm.addEventListener('submit', addSource);

}


// ----- DOM Loaded ----- //

document.addEventListener('DOMContentLoaded', setup);
