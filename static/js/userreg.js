console.log("hello working");

let id = (id) => document.getElementById(id);
let classes = (classes) => document.getElementsByClassName(classes);

let username = id("username"),
	fname = id("fname"),
	lname = id("lname"),
	email = id("email"),
	pwd = id("password"),
	pwd2 = id("password2"),
	dob = id("dob"),
	mob = id("mobile"),
	place = id("place"),
	acc = id("acc_type"),
	amt = id("deposit"),
	form=id("form"),

	errorMsg=classes("error"),
	successIcon=classes("success-icon"),
	failureIcon=classes("failure-icon");
formtag=document.querySelector("form");	
console.log(form);
console.log(errorMsg);
console.dir(errorMsg);

let engine = (id,serial,message) => {
	if (id.value.trim() === ""){
		errorMsg[serial].innerHTML = message;
		id.style.border = "2px solid red";

		failureIcon[serial].style.opacity = "1";
		successIcon[serial].style.opacity = "0";
	}
	else{
		errorMsg[serial].innerHTML = "";
		id.style.border = "2px solid green";

		failureIcon[serial].style.opacity = "0";
		successIcon[serial].style.opacity = "1";

	}
}

form.addEventListener("submit", (e) => {
	e.preventDefault();

	console.log("working");
	

	engine(username, 0, "Username cannot be blank");
	engine(fname,1,"First name Cannnot be blank");
	engine(lname,2,"Last name Cannnot be blank");
	engine(email,3,"Email cannot be blank");
	engine(pwd,4,"Password name Cannnot be blank");
  	engine(pwd2, 5, "Password cannot be blank");
  	engine(dob,6,"date of Birth Cannnot be blank");
  	engine(mob,7,"Mobile Number Cannnot be blank");
  	engine(place,8,"Location Cannnot be blank");
  	engine(acc,9,"Cannnot be blank");
  	engine(amt,10,"Ammount Cannnot be blank");
  	console.dir(e.target[0].value);
  	console.dir(e.target[1].value);
  	console.dir(e.target[2].value);
  	console.dir(e.target[3].value);
  	console.dir(e.target[4].value);
  	console.dir(e.target[5].value);
  	console.dir(e.target[6].value);
  	console.dir(e.target[7].value);
  	console.dir(e.target[8].value);
  	console.dir(e.target[9].value);
  	console.dir(e.target[10].value);
  
});
