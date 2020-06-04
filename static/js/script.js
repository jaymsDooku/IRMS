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
	var SeeUserRolesBtn = document.getElementById('SeeUserRolesBtn');
	if (SeeUserRolesBtn != null) {
		SeeUserRolesBtn.onclick = function(event) {
			switchBody('listUsers', listUsersInit);	
			changeNavBarItem(SeeUserRolesBtn);
		}
	}

	var notificationsBtn = document.getElementById('notificationsBtn');
	if (notificationsBtn != null) {
		notificationsBtn.onclick = function(event) {
			var sideBar = document.getElementsByClassName('sidebar')[0];
			sideView.open(sideBar);

			setOutstandingNotifications(0);

			event.stopPropagation();
		}

		var container = document.getElementsByClassName('container')[0];
		container.onclick = function() {
			sideView.close();
		}
	}
}

function setOutstandingNotifications(count) {
	var outstandingNotifications = document.getElementById('outstandingNotifications');
	if (count == 0) {
		outstandingNotifications.innerText = '';
	} else {
		outstandingNotifications.innerText = '(' + count + ')';
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

function autocomplete(inp, arr) {
	/*the autocomplete function takes two arguments,
	the text field element and an array of possible autocompleted values:*/
	var currentFocus;
	/*execute a function when someone writes in the text field:*/
	inp.addEventListener("input", function(e) {
	  var a, b, i, val = this.value;
	  /*close any already open lists of autocompleted values*/
	  closeAllLists();
	  if (!val) { return false;}
	  currentFocus = -1;
	  /*create a DIV element that will contain the items (values):*/
	  a = document.createElement("DIV");
	  a.setAttribute("id", this.id + "autocomplete-list");
	  a.setAttribute("class", "autocomplete-items");
	  /*append the DIV element as a child of the autocomplete container:*/
	  this.parentNode.appendChild(a);
	  /*for each item in the array...*/
	  for (i = 0; i < arr.length; i++) {
	    /*check if the item starts with the same letters as the text field value:*/
	    var arrEl = arr[i];
	    var name = arrEl.name;
	    if (name.substr(0, val.length).toUpperCase() == val.toUpperCase()) {
	      /*create a DIV element for each matching element:*/
	      b = document.createElement("DIV");
	      /*make the matching letters bold:*/
	      b.innerHTML = "<strong>" + name.substr(0, val.length) + "</strong>";
	      b.innerHTML += name.substr(val.length);
	      /*insert a input field that will hold the current array item's value:*/
	      b.innerHTML += "<input type='hidden' data-user='"  + arrEl.id + "' value='" + name + "'>";
	      /*execute a function when someone clicks on the item value (DIV element):*/
	      b.addEventListener("click", function(e) {
	          /*insert the value for the autocomplete text field:*/
	          var autocompleteTxt = this.getElementsByTagName("input")[0];
	          console.log(autocompleteTxt);
	          inp.value = autocompleteTxt.value;
	          inp.dataset.user = autocompleteTxt.user;
	          /*close the list of autocompleted values,
	          (or any other open lists of autocompleted values:*/
	          closeAllLists();
	      });
	      a.appendChild(b);
	    }
	  }
	});

	inp.onfocus = function(event) {
		inp.value = "";
	}

	inp.onblur = function(event) {
		console.log('hi');
		if (inp.dataset.user == undefined) {
			inp.value = "No One";
		}
	}
	/*execute a function presses a key on the keyboard:*/
	inp.addEventListener("keydown", function(e) {
	  var x = document.getElementById(this.id + "autocomplete-list");
	  if (x) x = x.getElementsByTagName("div");
	  if (e.keyCode == 40) {
	    /*If the arrow DOWN key is pressed,
	    increase the currentFocus variable:*/
	    currentFocus++;
	    /*and and make the current item more visible:*/
	    addActive(x);
	  } else if (e.keyCode == 38) { //up
	    /*If the arrow UP key is pressed,
	    decrease the currentFocus variable:*/
	    currentFocus--;
	    /*and and make the current item more visible:*/
	    addActive(x);
	  } else if (e.keyCode == 13) {
	    /*If the ENTER key is pressed, prevent the form from being submitted,*/
	    e.preventDefault();
	    if (currentFocus > -1) {
	      /*and simulate a click on the "active" item:*/
	      if (x) x[currentFocus].click();
	    }
	  }
	});
	function addActive(x) {
	/*a function to classify an item as "active":*/
	if (!x) return false;
	/*start by removing the "active" class on all items:*/
	removeActive(x);
	if (currentFocus >= x.length) currentFocus = 0;
	if (currentFocus < 0) currentFocus = (x.length - 1);
	/*add class "autocomplete-active":*/
	x[currentFocus].classList.add("autocomplete-active");
	}
	function removeActive(x) {
	/*a function to remove the "active" class from all autocomplete items:*/
	for (var i = 0; i < x.length; i++) {
	  x[i].classList.remove("autocomplete-active");
	}
	}
	function closeAllLists(elmnt) {
	/*close all autocomplete lists in the document,
	except the one passed as an argument:*/
	var x = document.getElementsByClassName("autocomplete-items");
	for (var i = 0; i < x.length; i++) {
	  if (elmnt != x[i] && elmnt != inp) {
	    x[i].parentNode.removeChild(x[i]);
	  }
	}
	}
	/*execute a function when someone clicks in the document:*/
	document.addEventListener("click", function (e) {
	  closeAllLists(e.target);
	});
}

function raiseIncidentInitNormal(incidentOnBehalf) {
	var incidentTitle = document.getElementById('incidentTitle');
	var incidentDescription = document.getElementById('incidentDescription');
	var incidentIdentification = document.getElementById('incidentIdentification');
	var incidentImplementation = document.getElementById('incidentImplementation');
	var impactSelect = document.getElementById('impactSelect');
	var severitySelect = document.getElementById('severitySelect');
	var systemSelect = document.getElementById('systemSelect');
	var prioritySelect = document.getElementById('prioritySelect');
	var departmentSelect = document.getElementById('departmentSelect');
	var teamSelect = document.getElementById('teamSelect');
	var submitBtn = document.getElementById('submitIncidentBtn');

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
		var severity = severitySelect.value;
		var system = systemSelect.value;
		var priority = prioritySelect.value;
		var team = teamSelect.value;

		var data = {
			title: title,
			description: description,
			identificationDeadline: identificationTime,
			implementationDeadline: implementationTime,
			impact: impact,
			severity: severity,
			system: system,
			priority: priority,
			team: team,
		};
		if (incidentOnBehalf != null) {
			var onBehalf = incidentOnBehalf.dataset.user;
			data['onBehalf'] = onBehalf;
		}
		console.log(data);
		post(data, 'raiseIncident', function(xhttp) {
			switchBody('listIncidents', listIncidentsInit);
			changeNavBarItem(document.getElementById('yourIncidentsBtn'))
		});
	}
}

function raiseIncidentInit() {
	var incidentOnBehalf = document.getElementById('incidentOnBehalf');
	if (incidentOnBehalf != null) {
		get('allUsers', function(xhttp) {
			var responseJson = JSON.parse(xhttp.responseText);
			var users = responseJson.users;
			autocomplete(incidentOnBehalf, users);
			raiseIncidentInitNormal(incidentOnBehalf);
		});
	} else {
		raiseIncidentInitNormal(null);
	}
}

var oldValues = {};

function initViewIncidentSelect(elId, valueType) {
	var select = document.getElementById(elId);
	select.onfocus = function(event) {
		oldValues[valueType] = select.value;
	}
	select.onchange = function(event) {
		var incidentId = select.dataset.incident;
		var newValue = select.value;
		showJustificationOverlay(incidentId, oldValues[valueType], newValue, valueType);
		oldValues[valueType] = newValue;
	}
}

function viewIncidentInit() {
	var followText = document.getElementById('followText');
	initFollowButton(followText.parentNode.dataset.incident, followText);

	initViewIncidentSelect('prioritySelect', 'priority');
	initViewIncidentSelect('impactSelect', 'impact');
	initViewIncidentSelect('severitySelect', 'severity');

	var identifiedBtn = document.getElementById('identifiedBtn');
	if (identifiedBtn != null) {
		identifiedBtn.onclick = function(event) {
			var incidentId = identifiedBtn.dataset.incident;
			get('resolutionIdentified/' + incidentId, function(xhttp) {
				var responseJson = JSON.parse(xhttp.responseText);

				identifiedBtn.parentNode.innerHTML = '<div class="irms-header"><p>Date Identified</p></div><div class="irms-text"><p>' + responseJson.date + '</p></div>';

				var incidentStatus = document.getElementById('incidentStatus');
				incidentStatus.classList.remove(1);
				incidentStatus.classList.add(responseJson.status_class);
				incidentStatus.innerText = responseJson.status;
			});
		}
	}

	var implementedBtn = document.getElementById('implementedBtn');
	if (implementedBtn) {
		implementedBtn.onclick = function(event) {
			var incidentId = implementedBtn.dataset.incident;
			get('resolutionImplemented/' + incidentId, function(xhttp) {
				var responseJson = JSON.parse(xhttp.responseText);

				implementedBtn.parentNode.innerHTML = '<div class="irms-header"><p>Date Implemented</p></div><div class="irms-text"><p>' + responseJson.date + '</p></div>';

				var incidentStatus = document.getElementById('incidentStatus');
				incidentStatus.classList.remove(1);
				incidentStatus.classList.add(responseJson.status_class);
				incidentStatus.innerText = responseJson.status;
			});
		}
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

	var noteItems = document.getElementsByClassName('incident-note');
	domUtil.onClick(noteItems, function(event) {
		var noteId = this.dataset.note;
		viewIncidentPageItem(noteId, 'Note', function() {
		});
	});

	var questionItems = document.getElementsByClassName('incident-question');
	domUtil.onClick(questionItems, function(event) {
		var questionId = this.dataset.question;
		viewIncidentPageItem(questionId, 'Question', function() {
			var submitAnswerBtn = document.getElementById('submitAnswerBtn');
			submitAnswerBtn.onclick = function(event) {
				var questionId = submitAnswerBtn.dataset.question;
				var answerContent = document.getElementById('answerContent');
				var answer = answerContent.value;

				var data = {
					answer: answer
				};

				post(data, 'answerQuestion/' + questionId, function(xhttp) {
					viewIncidentPageItem(questionId, 'Question', function() {
					});
				});
			}
		});
	});

	var taskItems = document.getElementsByClassName('incident-task');
	for (var i = 0; i < taskItems.length; i++) {
		var taskItem = taskItems[i];

		var departmentSelect = domUtil.getElementByClassName(taskItem, 'task-department-select');
		var teamSelect = domUtil.getElementByClassName(taskItem, 'task-team-select');
		initDepartmentSelect(departmentSelect, teamSelect);

		var assignTaskTeamBtn = domUtil.getElementByClassName(taskItem, 'assign-task-team-btn');
		assignTaskTeamBtn.onclick = function(event) {
			var incidentId = assignTaskTeamBtn.dataset.incident;
			var teamOption = teamSelect.options[teamSelect.selectedIndex];
			var teamId = teamOption.dataset.team;
			get('requestIncidentTeam/' + incidentId + '/' + teamId, function(xhttp) {
				var teamsAssigned = domUtil.getElementByClassName(taskItem, 'assign-task-team-btn');
				teamsAssigned.innerHTML += '<div class="incident-tag"><p>' + teamOption.value + '</p></div>';
				console.log('hello');
			});
		}
	}

	var newNoteBtn = document.getElementById('newNoteBtn').parentNode;
	newNoteBtn.onclick = function(event) {
		var addNoteBtn = document.getElementById('addNoteBtn');
		addNoteBtn.onclick = function(event) {
			addIncidentItem('note', 'Note');
		}

		showOverlay('note-form-container');
	}

	var newQuestionBtn = document.getElementById('newQuestionBtn').parentNode;
	newQuestionBtn.onclick = function(event) {
		var askQuestionBtn = document.getElementById('askQuestionBtn');
		askQuestionBtn.onclick = function(event) {
			addIncidentItem('question', 'Question');
		}

		showOverlay('question-form-container');
	}

	var newTaskBtn = document.getElementById('newTaskBtn').parentNode;
	newTaskBtn.onclick = function(event) {
		var addTaskBtn = document.getElementById('addTaskBtn');
		addTaskBtn.onclick = function(event) {
			addIncidentItem('task', 'Task');
		}

		showOverlay('task-form-container');
	}

	var overlay = document.getElementById('overlay');
	overlay.onclick = function(event) {
		hideOverlay();
	}

	var overlayBody = document.getElementById('overlay-body');
	overlayBody.onclick = function(event) {
		event.stopPropagation();
	}
}

function viewIncidentPageItem(id, itemType, callback) {
	get('view' + itemType + '/' + id, function(xhttp) {
		var overlayViewContainer = document.getElementsByClassName('overlay-view-container')[0];
		overlayViewContainer.innerHTML = xhttp.responseText;

		callback();
		showOverlay('overlay-view-container');
	});
}

function addIncidentItem(itemType, item) {
	var incidentId = addNoteBtn.dataset.incident;

	var titleItem = document.getElementById(itemType + 'Title');
	var title = titleItem.value;

	var contentItem = document.getElementById(itemType + 'Content');
	var content = contentItem.value;

	var data = {
		title: title,
		content: content
	};
	var verb = itemType == 'question' ? 'ask' : 'add';
	post(data, verb + item + '/' + incidentId, function(xhttp) {
		switchBody('viewIncident/' + incidentId, viewIncidentInit);
	});
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

		console.log(valueType);
		post(data, 'changeIncidentValue/' + incidentId + '/' + valueType, function(xhttp) {
			hideOverlay();

			var select = document.getElementById(valueType + 'Select');
			var pending = domUtil.getElementByClassName(select.parentNode, 'pending');
			console.log(pending);
			pending.innerText = "*";
		});
	}

	showOverlay('request-justification-container');
}

function listIncidentsInit() {
	var incidentItems = document.getElementsByClassName('incident-item');
	if (incidentItems.length == 1 && incidentItems[0].classList.contains('no-incidents')) {
		return;
	}

	for (var i = 0; i < incidentItems.length; i++) {
		var incidentItem = incidentItems[i];
		var incidentId = incidentItem.dataset.incident;
		incidentItem.onclick = function(event) {
			switchBody('viewIncident/' + incidentId, viewIncidentInit);
		}

		var followText = domUtil.getElementByClassName(incidentItem, 'follow-text');
		initFollowButton(incidentId, followText);
	}
}

function initFollowButton(incidentId, followText) {
	var followBtn = followText.parentNode;
	followBtn.onclick = function(event) {
		if (followText.innerText == "Follow") {
			get('followIncident/' + incidentId, function() {
				followText.innerText = "Following";
				followBtn.classList.add('following');
			});
			event.stopPropagation();
		}
	}
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

				event.stopPropagation();
			}
		}

		var approveBtn = domUtil.getElementByClassName(requestItem, 'approve-btn');
		var denyBtn = domUtil.getElementByClassName(requestItem, 'deny-btn');
		if (approveBtn != null) {
			approveBtn.onclick = function(event) {
				decideRequest(requestItem, 'approve');

				approveBtn.remove();
				denyBtn.remove();
				event.stopPropagation();
			}
		}

		if (denyBtn != null) {
			denyBtn.onclick = function(event) {
				decideRequest(requestItem, 'deny')

				approveBtn.remove();
				denyBtn.remove();
				event.stopPropagation();
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
function listUsersInit() {
	var roleDropdowns = document.getElementsByClassName('role-dropdown');
	for (var i = 0; i < roleDropdowns.length; i++) {
		var dropdown = roleDropdowns[i];
		dropdown.onchange = function(event) {
			var chosenRole = this.value;
			var userId = this.dataset.user;

			var data = {
				role: chosenRole
			};
			var path = 'updateRole/' + userId;
			console.log(path);
			console.log(data);
			post(data, path, function(xhttp) {
			});
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
		var changeRequestId = requestItem.dataset.changerequest;
		path = 'decideChangeRequest/' + changeRequestId;
	}

	get(path + '/' + decision, function(xhttp) {
	});
}

function showOverlay(content_class) {
	var overlayBody = document.getElementById('overlay-body');
	var children = overlayBody.children;
	for (var i = 0; i < children.length; i++) {
		var child = children[i];
		if (child.classList.contains(content_class)) {
			child.style.display = "block";
		} else {
			child.style.display = "none";
		}
	}

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

	setInterval(function() {
		get('notifications', function(xhttp) {
			var responseJson = JSON.parse(xhttp.responseText);

			var unseen = responseJson.unseen;
			setOutstandingNotifications(parseInt(unseen));

			var sidebarBody = document.getElementsByClassName('sidebar-body')[0];
			console.log(responseJson);
			sidebarBody.innerHTML = responseJson.body;
			console.log('notification update');
		})
	}, 5000);
}