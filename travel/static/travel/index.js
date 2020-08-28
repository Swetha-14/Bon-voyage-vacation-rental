// Slideshow
var slideIndex = 1;
showDivs(slideIndex);

function plusDivs(n) {
  showDivs(slideIndex += n);
}

function showDivs(n) {
  var i;
  var x = document.getElementsByClassName("mySlides");
  if (n > x.length) {slideIndex = 1}
  if (n < 1) {slideIndex = x.length}
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";  
  }
  x[slideIndex-1].style.display = "block";  
}

// To clamp the text
var p=document.getElementsByClassName('para')[0],
lineheight=parseInt(window.getComputedStyle(p).getPropertyValue("line-height"));
var lines=Math.floor(200/lineheight);
p.style['-webkit-line-clamp']=lines;
