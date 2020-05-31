const API_URL = "http://127.0.0.1:5000/";

const DONE = 4;

const HTTP_CREATED = 201;
const HTTP_OKAY = 200;
const HTTP_DELETED = 204;

function successful(status) {
    return status >= 200 && status < 300;
}

function Headers(method, contentType) {
    this.method = method;
    this.contentType = contentType !== undefined ? contentType : 'application/json';
}

function postNoData(path, callback) {
    post(null, path, callback);
}

function get(path, callback) {
    send(null, path, new Headers("GET"), callback);
}

function post(object, path, callback) {
    send(object, path, new Headers("POST"), callback);
}

function send(object, path, headers, callback) {
    ajax(object, API_URL + path, headers, callback);
}

function ajax(object, url, headers, callback) {
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState == DONE && successful(this.status)) {
            callback(xhttp);
        }
    }
    xhttp.open(headers.method, url, true);

    if (object) {
        xhttp.setRequestHeader("Content-Type", headers.contentType);
        var data = JSON.stringify(object);
        xhttp.send(data);
    } else {
        xhttp.send();
    }
}