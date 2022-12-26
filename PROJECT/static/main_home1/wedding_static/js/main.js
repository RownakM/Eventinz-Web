

var views = [
  "grid",
  "list_view",
  "map"
];
var visibleDivId = null;
function togg(divId) {
  if (visibleDivId === views) {
    //visibleDivId = null;
  } else {
    visibleDivId = divId;
  }
  hideNonVisibleDivs();
}


$(".event-deal .grid_list_btn").click(function () {
  $('.event-deal .grid_list_btn').show();
  $(this).hide();
});


function hideNonVisibleDivs() {
  var i, divId, div;
  for (i = 0; i < views.length; i++) {
    divId = views[i];
    div = document.getElementById(divId);
    if (visibleDivId === divId) {
      div.style.display = "block";
    } else {
      div.style.display = "none";
    }
  }
}


let actmenu = ".grd_ev"

$(actmenu).on("click", function () {
  $(actmenu).removeClass("grid_active", "otl_btn");
  $(this).addClass("grid_active")
})

let actmenu1 = ".grd_ev_1"

$(actmenu1).on("click", function () {
  $(actmenu1).removeClass("grid_active", "otl_btn");
  $(this).addClass("grid_active")
})



var selector = ".sdm_bg";

$(selector).on("click", function () {
  $(selector).removeClass("sdb_active");
  $(this).addClass("sdb_active");
});




$(document).ready(function () {
  $(".vendor_carousel").owlCarousel({
    items: 1,
    loop: true,
    margin: 30,
    dots: true,
    autoplay: false,
    autoplayTimeout: 1000,
    autoplayHoverPause: true,
    nav: false,
    responsiveClass: true,
    responsive: {
      0: {
        items: 1,
      },
      600: {
        items: 2,
      },
      1000: {
        items: 3,
        loop: true,
        margin: 30,
      },
      1200: {
        items: 4,
        loop: true,
        margin: 30,
      },
    },
  });
});

$(document).ready(function () {
  $(".wedding_carousel").owlCarousel({
    items: 1,
    loop: true,
    margin: 30,
    dots: true,
    autoplay: false,
    autoplayTimeout: 1000,
    autoplayHoverPause: true,
    nav: false,
    responsiveClass: true,
    responsive: {
      0: {
        items: 1,
      },
      600: {
        items: 2,
      },
      1000: {
        items: 3,
        loop: true,
        margin: 30,
      },
      1200: {
        items: 3,
        loop: true,
        margin: 30,
      },
    },
  });
});


$(document).ready(function () {
  $(".review_carousel").owlCarousel({
    items: 1,
    loop: true,
    margin: 30,
    dots: true,
    autoplay: false,
    autoplayTimeout: 1000,
    autoplayHoverPause: true,
    nav: false
  });
});




var divs = ["photos", "tours"];
var visibleDivId = null;
function divVisibility(divId) {
  if(visibleDivId === divId) {
    visibleDivId = null;
  } else {
    visibleDivId = divId;
  }
  hideNonVisibleDivs1();
}
function hideNonVisibleDivs1() {
  var i, divId, div;
  for(i = 0; i < divs.length; i++) {
    divId = divs[i];
    div = document.getElementById(divId);
    if(visibleDivId === divId) {
      div.style.display = "block";
    } else {
      div.style.display = "none";
    }
  }
}


var overview = ["details", "faqs", "pricing"];
var visibleDivId = null;
function overviewvisibility(divId) {
  if(visibleDivId === divId) {
    visibleDivId = null;
  } else {
    visibleDivId = divId;
  }
  hidoverviewvisibleDiv();
}
function hidoverviewvisibleDiv() {
  var i, divId, div;
  for(i = 0; i < overview.length; i++) {
    divId = overview[i];
    div = document.getElementById(divId);
    if(visibleDivId === divId) {
      div.style.display = "block";
    } else {
      div.style.display = "none";
    }
  }
}






