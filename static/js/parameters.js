/* http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript/901144#901144 */
window.parameters = {};
(window.onpopstate = function () {
    var match,
        pl = /\+/g,
        search = /([^&=]+)=?([^&]*)/g,
        decode = function (s) { return decodeURIComponent(s.replace(pl, " ")); },
        query = window.location.search.substring(1);
    while (match = search.exec(query))
       window.parameters[decode(match[1])] = decode(match[2]);
})();
