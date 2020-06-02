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
			changeModeOnClick(userModeBtn, 'userNavBar', function() {
				var raiseIncidentBtn = document.getElementById('raiseIncidentBtn');
				changeNavBarItem(raiseIncidentBtn);
				raiseIncidentBtn.click();
			});
		}
	}
	if (managerModeBtn != null) {
		managerModeBtn.onclick = function(event) {
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
	if (btn != null && btn.classList.contains('navbar-selected')) {
		return;
	}

	var ul = document.querySelector('.navbar-items ul');
	var selectedItem = domUtil.getElementByClassName(ul, 'navbar-selected');
	selectedItem.classList.remove('navbar-selected');
	if (btn != null) {
		btn.classList.add('navbar-selected');
	}
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
	if (allRequestsBtn != null) {
		allRequestsBtn.onclick = function(event) {
			switchBody('allChangeRequests', listRequestsInit);
			changeNavBarItem(allRequestsBtn);
		}
	}

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
	if (yourRequestsBtn != null) {
		yourRequestsBtn.onclick = function(event) {
			switchBody('listChangeRequests', listRequestsInit);	
			changeNavBarItem(yourRequestsBtn);
		}
	}
}

function initDepartmentSelect(departmentSelect, teamSelect) {
	departmentSelect.onchange = function(event) {
		get('departmentTeams/' + departmentSelect.value, function(xhttp) {
			var responseJson = JSON.parse(xhttp.responseText);

			while (teamSelect.options.length) {
				teamSelect.remove(0);
			}

			var newTeams = responseJson.teams;
			for (var i = 0; i < newTeams.length; i++) {
				var team = newTeams[i];
				var teamOption = new Option(team.team_name, i);
				teamOption.dataset.team = team.team_id
				teamSelect.options.add(teamOption);
			}
		});
	}
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

	initDepartmentSelect(departmentSelect, teamSelect);
	
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
			changeNavBarItem(document.getElementById('yourIncidentsBtn'))
		});
	}
}

var oldPriority;

function viewIncidentInit() {
	var prioritySelect = document.getElementById('prioritySelect');
	prioritySelect.onfocus = function(event) {
		oldPriority = prioritySelect.value;
	}
	prioritySelect.onchange = function(event) {
		var incidentId = prioritySelect.dataset.incident;
		var newPriority = prioritySelect.value;
		showJustificationOverlay(incidentId, oldPriority, newPriority, 'priority');
		oldPriority = newPriority;
	}

	var departmentSelect = document.getElementById('departmentSelect');
	var teamSelect = document.getElementById('teamSelect');
	initDepartmentSelect(departmentSelect, teamSelect);

	var assignTeamBtn = document.getElementById('assignTeamBtn');
	assignTeamBtn.onclick = function(event) {
		var incidentId = assignTeamBtn.dataset.incident;
		var teamOption = teamSelect.options[teamSelect.selectedIndex];
		var teamId = teamOption.dataset.team;
		get('requestIncidentTeam/' + incidentId + '/' + teamId, function(xhttp) {
			var responseJson = JSON.parse(xhttp.responseText);

			var teamAssignedTable = document.getElementById('teamAssignedTableBody');
			teamAssignedTable.innerHTML += ("<tr>" +
				"<td>" + responseJson.name + "</td>" +
				"<td>" + responseJson.date_issued + "</td>" +
				"<td>" + responseJson.assigner + "</td>" +
				"<td>" + responseJson.status + "</td>" +
				"</tr>");
		});
	}
}

function showJustificationOverlay(incidentId, oldValue, newValue, valueType) {
	var requestChangeBtn = document.getElementById('requestChangeBtn');
	requestChangeBtn.onclick = function(event) {
		var requestJustification = document.getElementById('requestJustification');
		var justification = requestJustification.value;

		var data = {
			oldValue: oldValue,
			newValue: newValue,
			justification: justification
		};

		post(data, 'changeIncidentValue/' + incidentId + '/' + valueType, function(xhttp) {
			console.log('hiding overlay');
			hideOverlay();
		});
	}

	showOverlay();
}

function listIncidentsInit() {
	var incidentItems = document.getElementsByClassName('incident-item');
	if (incidentItems.length == 1 && incidentItems[0].classList.contains('no-incidents')) {
		return;
	}

	domUtil.onClick(incidentItems, function(event) {
		var incidentId = this.dataset.incident;
		switchBody('viewIncident/' + incidentId, viewIncidentInit);
	});
}

var justificationVisible = {};

function listRequestsInit() {
	var requestItems = document.getElementsByClassName('request-item');
	if (requestItems.length == 1 && requestItems[0].classList.contains('no-requests')) {
		return;
	}

	for (var i = 0; i < requestItems.length; i++) {
		var requestItem = requestItems[i];
		var changeRequestId = requestItem.dataset.changerequest;

		requestItem.onclick = function(event) {
			var justificationEl = domUtil.getElementByClassName(this, 'request-justification');
			if (justificationEl == null) {
				return;
			}
			if (!(changeRequestId in justificationVisible) || !justificationVisible[changeRequestId])  {
				justificationEl.style.display = "block";
	            justificationEl.animate([
	                    { opacity: 0 },
	                    { opacity: 1 }
	                ], { duration: 1000, iterations: 1 });
	            justificationEl.style.opacity = "1";
	            justificationVisible[changeRequestId] = true;
	        } else {
	            justificationEl.animate([
	                    { opacity: 1 },
	                    { opacity: 0 }
	                ], { duration: 1000, iterations: 1 });
	            justificationEl.style.opacity = "0";
	            justificationEl.style.display = "none";
	            justificationVisible[changeRequestId] = false;
	        }
		}

		var viewIncidentBtn = domUtil.getElementByClassName(requestItem, 'view-incident-btn');
		if (viewIncidentBtn != null) {
			viewIncidentBtn.onclick = function(event) {
				var incidentId = requestItem.dataset.incident;
				switchBody('viewIncident/' + incidentId, viewIncidentInit);
			}
		}

		var approveBtn = domUtil.getElementByClassName(requestItem, 'approve-btn');
		if (approveBtn != null) {
			approveBtn.onclick = function(event) {
				decideRequest(requestItem, 'approve');
			}
		}

		var denyBtn = domUtil.getElementByClassName(requestItem, 'deny-btn');
		if (denyBtn != null) {
			denyBtn.onclick = function(event) {
				decideRequest(requestItem, 'deny')
			}
		}
	}

	var teamAssignmentsBtn = document.getElementById('teamAssignmentsBtn');
	teamAssignmentsBtn.onclick = function(event) {
		var pageTitle = document.getElementById('pageTitle');
		if (pageTitle.innerText == "Your Incidents") {
			switchBody('listTeamAssignmentRequests', listRequestsInit);
		} else {
			switchBody('allTeamAssignmentRequests', listRequestsInit);
		}
	}

	var valueChangesBtn = document.getElementById('valueChangesBtn');
	valueChangesBtn.onclick = function(event) {
		var pageTitle = document.getElementById('pageTitle');
		if (pageTitle.innerText == "Your Incidents") {
			switchBody('listChangeRequests', listRequestsInit);
		} else {
			switchBody('allChangeRequests', listRequestsInit);
		}
	}
}

function decideRequest(requestItem, decision) {
	var requestTypesEl = document.getElementsByClassName('request-types')[0];
	var selectedTab = domUtil.getElementByClassName(requestTypesEl, 'selected-tab');
	var requestStatus = domUtil.getElementByClassName(requestItem, 'request-status');

	requestStatus.classList.remove('pending-tag');
	if (decision == 'approve') {
		requestStatus.classList.add('approved-tag');
		requestStatus.innerText = "Approved";
	} else {
		requestStatus.classList.add('denied-tag');
		requestStatus.innerText = "Denied";
	}

	var path;
	if (selectedTab.id == "teamAssignmentsBtn") {
		var incidentId = requestItem.dataset.assignedto;
		var teamId = requestItem.dataset.team;
		path = 'decideIncidentTeam/' + incidentId + '/' + teamId;
	} else if (selectedTab.id == "valueChangesBtn") {
		path = 'decideChangeRequest/' + changeRequestId;
	}

	get(path + '/' + decision, function(xhttp) {
	});
}

function showOverlay() {
	document.getElementById("overlay").style.display = "block";
}

function hideOverlay() {
	document.getElementById("overlay").style.display = "none";
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