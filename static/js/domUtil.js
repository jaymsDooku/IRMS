var domUtil = (function() {

    var m = { };
    m.getElementByClassName = function(element, className) {
        var children = element.getElementsByClassName(className);
        return children.length > 0 ? children[0] : null;
    }

    m.onHover = function(elements, mouseoverCallback, mouseoutCallback) {
        for (var i = 0; i < elements.length; i++) {
            var el = elements[i];
            el.onmouseover = mouseoverCallback;
            el.onmouseout = mouseoutCallback;
        }
    }

    m.onClick = function(elements, callback) {
        for (var i = 0; i < elements.length; i++) {
            var el = elements[i];
            el.onclick = callback;
        }
    }

    return m;
})();