function calcTotal()
{
	var unitPrice = document.getElementById('unit').innerHTML;
	var qty = document.getElementById('numb').value;
	
	var total = unitPrice*qty;
	//var t = total.toString();
	//localStorage.setItem("t", t);
	window.name = total.toString()
	document.getElementById('total').innerHTML = total;
}

function showTime() {
	$('footer #time').text(Date());
}

function thisOne()
	{
		var shit = document.getElementById('amount');
		var also = document.getElementById('paybtn');
		var carstatus = document.getElementById('cartstat');
		if(shit.innerHTML == 0)
		{
			also.className += " disabled";
			carstatus.innerHTML = "Cart Empty";
		}
	}

function verifyForm()
{
	if(document.forms['loginform']['username'].value == "" )
		alert("Please enter username.");
	else if(document.forms['loginform']['password'].value == "")
		alert("Please enter password");
}

function verifyRegForm()
{
	if(document.forms['regform']['username'].value == "")
		alert("Please enter unique username");
	else if(document.forms['regform']['email'].value == "")
		alert("Please enter email");
	else if(document.forms['regform']['password'].value == "")
		alert("Please enter password");
	else
		alert("Username already taken.");
}


function buyItem()
{
	$.ajax({
	        url: "",
	        type: 'GET',
	        dataType: 'json', // added data type
	        success: function(res) {
	            console.log(res);
	            alert(res);
	        }
	    });
}

function verifyNumber()
{
	var target = document.getElementById('numb').value;
	var target1 = document.getElementById('verbtn');


	if(target == "" || target == 0)
		alert("Please choose quantity");
	else if(Number(target) > Number(document.getElementById('maxiq').innerHTML))
		alert("Insufficient stock. Reduce quantity");
	else if(Number(target) < 0)
		alert("Invalid quantity");
	else
	{
		target1.innerHTML = "Done";

		document.getElementById('disbtn').className += " hidden";
	}
}
setInterval(showTime, 1000);
