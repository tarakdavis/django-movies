var queryString = window.location.search;

queryString = queryString.substring(1);

var parseQueryString = function(queryString){
  var params = {}, queries, temp, i, l;

  queries = queryString.split("&amp;");

  for (i=0, l=queries.length; i<l; i++) {
    temp = queries[i].split('=');
    params[temp[0]] = temp[1];
  }
  return params;
};

var params = parseQueryString;
var a=5
var a
