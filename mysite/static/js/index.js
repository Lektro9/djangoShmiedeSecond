var definitionList = $('dl');
var counter = 1;
var cardSum = $('dl card').length;

$('#testCount').html(counter + "/" + cardSum)

definitionList.on('init', function(){
  //$('.slick-current', this).addClass('flip');
})

definitionList.slick({
  centerMode: true,
  arrows: false,
  centerPadding: '20px',
  slidesToShow: 3,
  responsive: [{
      breakpoint: 950,
      settings: {
        slidesToShow: 1,
        centerPadding: '10px'
      }
  }]
});

	definitionList.on('beforeChange',function(){
	  $('.slick-slide', this).removeClass('flip')
	});

	definitionList.on('afterChange', function(){
	  counter = $("div[class='slick-track'] div[class~='slick-center']").not("div[class~='slick-cloned']").attr("data-slick-index")
	  counter = parseInt(counter)+1;
	  $('#testCount').html(counter + "/" + cardSum)
	});

	definitionList.on('click', '.slick-current', function(){
	  $(this).toggleClass('flip')
	});

	$('#umkehren').click(function(){
	  $('card').each(function(){
	    var dt=$(this).find("dt").html();
	    $(this).find("dt").html($(this).find("dd").html());
	    $(this).find("dd").html(dt);
	  });
	});

	var slideIndex = cardSum;

	$('#loeschen').on('click', function() {
	  definitionList.slick('slickRemove', counter-1);
	  cardSum--;
	  if (cardSum < counter) {
	  	counter = cardSum
	  }
	  $("div[class~='slick-slide']").not("div[class~='slick-cloned']").each(function (index, value) {
	  	$(this).attr("data-slick-index", index)
	  });
	  $('#testCount').html(counter + "/" + cardSum)
	  checkCardAmount(cardSum);
	});

	$('#weiter').on('click', function() {
		definitionList.slick("slickNext")
	});

	function checkCardAmount(cardAmount){
		if (cardAmount < 1) {
			$("#testCount").html("Congrats!")
			var refreshButton = $('<div style="text-align:center;"> <button type="button" class="btn btn-primary" onClick="window.location.reload()" >Refresh</button></div>')
			$("#testCount").append(refreshButton);
	    }
	}
