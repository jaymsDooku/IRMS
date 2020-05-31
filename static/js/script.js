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
}

window.onload = function(event) {
	init(event);
}