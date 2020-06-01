function init(event) {
	var logoutBtn = document.getElementById('logoutBtn');
	if (logoutBtn != null) {
		logoutBtn.onclick = function(event) {
			get('logout', function(xhttp) {
				var responseJson = JSON.parse(xhttp.responseText);
				var status = responseJson.status;

				if (status == 'logout') {
					var container = document.getElementsByClassName('container')[0];
					container.innerHTML = responseJson.body;
					init();
				}
			});
		}
	}

	var username = document.getElementById('username');
	var password = document.getElementById('password');
	var loginBtn = document.getElementById('loginBtn');
	if (loginBtn != null) {
		loginBtn.onclick = function(event) {
			var userData = {
				username: username.value,
				password: password.value
			};
			post(userData, 'login', function(xhttp) {
				console.log(xhttp);
				var responseJson = JSON.parse(xhttp.responseText);
				var status = responseJson.status;

				if (status == 'invalid credential') {
					var error = document.getElementsByClassName('login-error')[0];
					error.style.display = "block";
		            error.animate([
		                    { opacity: 0 },
		                    { opacity: 1 }
		                ], { duration: 1000, iterations: 1 });
		            error.style.opacity = "1";
					return; 
				}

				if (status == 'success') {
					var body = responseJson.body;
					var container = document.getElementsByClassName('container')[0];
					container.innerHTML = body;
					init();
				}
			});
		}
	}

	var userModeBtn = document.getElementById('userModeBtn');
	var managerModeBtn = document.getElementById('managerModeBtn');
	if (userModeBtn != null) {
		userModeBtn.onclick = changeModeOnClick(userModeBtn, 'userNavBar');
	}
	if (managerModeBtn != null) {
		managerModeBtn.onclick = changeModeOnClick(managerModeBtn, 'managerNavBar');
	}

	navbarInit();
}

function navbarInit() {
	var raiseIncidentBtn = document.getElementById('raiseIncidentBtn');
	if (raiseIncidentBtn != null) {
		raiseIncidentBtn.onclick = function(event) {
			console.log('hello');
			get('/raiseIncident', function(xhttp) {
				var containerBody = document.getElementsByClassName('container-body')[0];
				containerBody.innerHTML = xhttp.responseText;
			});
		}
	}
	var yourIncidentsBtn = document.getElementById('yourIncidentsBtn');
	var yourRequestsBtn = document.getElementById('yourRequestsBtn');
}

function changeModeOnClick(btn, path)  {
	return function(event) {
		get(path, function(xhttp) {
			var ul = document.querySelector('.navbar-items ul');
			ul.innerHTML = xhttp.responseText;

			var selectedItem = domUtil.getElementByClassName(btn.parentNode, 'selected');
			selectedItem.classList.remove('selected');
			btn.classList.add('selected');

			navbarInit();
		});
	}
}

window.onload = function(event) {
	init(event);
}