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
		userModeBtn.onclick = function(event) {
			console.log('hello1');
			changeModeOnClick(userModeBtn, 'userNavBar', function() {
				var raiseIncidentBtn = document.getElementById('raiseIncidentBtn');
				changeNavBarItem(raiseIncidentBtn);
				raiseIncidentBtn.click();
			});
		}
	}
	if (managerModeBtn != null) {
		managerModeBtn.onclick = function(event) {
			console.log('hello1');
			changeModeOnClick(managerModeBtn, 'managerNavBar', function() {
				var allIncidentsBtn = document.getElementById('allIncidentsBtn');
				changeNavBarItem(allIncidentsBtn);
				allIncidentsBtn.click();
			});
		}
	}

	navbarInit();
	listIncidentsInit();
}

function switchBody(path, init) {
	get(path, function(xhttp) {
		var containerBody = document.getElementsByClassName('container-body')[0];
		containerBody.innerHTML = xhttp.responseText;
		init();
	});
}

function changeNavBarItem(btn) {
	if (btn.classList.contains('navbar-selected')) {
		return;
	}

	var ul = document.querySelector('.navbar-items ul');
	var selectedItem = domUtil.getElementByClassName(ul, 'navbar-selected');
	selectedItem.classList.remove('navbar-selected');
	btn.classList.add('navbar-selected');
}

function navbarInit() {
	var allIncidentsBtn = document.getElementById('allIncidentsBtn');
	if (allIncidentsBtn != null) {
		allIncidentsBtn.onclick = function(event) {
			switchBody('allIncidents', listIncidentsInit);
			changeNavBarItem(allIncidentsBtn);
		}
	}

	var allRequestsBtn = document.getElementById('allRequestsBtn');

	var raiseIncidentBtn = document.getElementById('raiseIncidentBtn');
	if (raiseIncidentBtn != null) {
		raiseIncidentBtn.onclick = function(event) {
			switchBody('raiseIncident', raiseIncidentInit);
			changeNavBarItem(raiseIncidentBtn);
		}
	}
	var yourIncidentsBtn = document.getElementById('yourIncidentsBtn');
	if (yourIncidentsBtn != null) {
		yourIncidentsBtn.onclick = function(event) {
			switchBody('listIncidents', listIncidentsInit);
			changeNavBarItem(yourIncidentsBtn);
		}
	}

	var yourRequestsBtn = document.getElementById('yourRequestsBtn');
}

function raiseIncidentInit() {
	var incidentTitle = document.getElementById('incidentTitle');
	var incidentDescription = document.getElementById('incidentDescription');
	var incidentIdentification = document.getElementById('incidentIdentification');
	var incidentImplementation = document.getElementById('incidentImplementation');
	var impactSelect = document.getElementById('impactSelect');
	var systemSelect = document.getElementById('systemSelect');
	var prioritySelect = document.getElementById('prioritySelect');
	var departmentSelect = document.getElementById('departmentSelect');
	var teamSelect = document.getElementById('teamSelect');
	var submitBtn = document.getElementById('submitIncidentBtn');

	/*console.log(incidentTitle);
	console.log(incidentDescription);
	console.log(incidentIdentification);
	console.log(incidentImplementation);
	console.log(impactSelect);
	console.log(systemSelect);
	console.log(prioritySelect);
	console.log(departmentSelect);
	console.log(teamSelect);
	console.log(submitBtn);*/

	if (incidentTitle == null || incidentDescription == null || incidentIdentification == null ||
		incidentImplementation == null || impactSelect == null || systemSelect == null || prioritySelect == null ||
		departmentSelect == null || teamSelect == null || submitBtn == null) {
		return;
	}
	
	submitBtn.onclick = function(event) {
		var title = incidentTitle.value;
		var description = incidentDescription.value;
		var identificationTime = incidentIdentification.value;
		var implementationTime = incidentImplementation.value;
		var impact = impactSelect.value;
		var system = systemSelect.value;
		var priority = prioritySelect.value;
		var team = teamSelect.value;

		var data = {
			title: title,
			description: description,
			identificationDeadline: identificationTime,
			implementationDeadline: implementationTime,
			impact: impact,
			system: system,
			priority: priority,
			team: team
		};
		post(data, 'raiseIncident', function(xhttp) {
			switchBody('listIncidents', listIncidentsInit);
		});
	}
}

function viewIncidentInit() {
}

function listIncidentsInit() {
	var incidentItems = document.getElementsByClassName('incident-item');
	if (incidentItems.length == 1 && incidentItems[0].children.length == 1) {
		return;
	}

	domUtil.onClick(incidentItems, function(event) {
		var incidentId = this.dataset.incident;
		switchBody('viewIncident/' + incidentId, viewIncidentInit);
	});
}

function changeModeOnClick(btn, path, callback)  {
	get(path, function(xhttp) {
		var ul = document.querySelector('.navbar-items ul');
		ul.innerHTML = xhttp.responseText;

		var selectedItem = domUtil.getElementByClassName(btn.parentNode, 'selected');
		selectedItem.classList.remove('selected');
		btn.classList.add('selected');

		navbarInit();
		callback();
	});
}

window.onload = function(event) {
	init(event);
}