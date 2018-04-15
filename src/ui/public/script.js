

function colourify(text, highlights){
  if (highlights.length == 0) return text;


  var colorified = text.slice(0, highlights[0][0])

  highlights.forEach(function(d, i){
    colorified += text.slice(d[0], d[1]).fontcolor(d[2]);
    if (i < highlights.length - 1)
      colorified += text.slice(d[1], highlights[i+1][0]);
    else
      colorified += text.slice(d[1], text.length);
  });

  return colorified;
}
