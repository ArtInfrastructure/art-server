.event-form {
	border: solid 3px #555; 
	position: absolute; top: 60px; left: 60px; width: 500px;
	padding: 10px; 
	background: #FFF;
}
.event-form .close-link { float: right; font-size: 1.4em; font-weight: bold; }
.event-form label { display: block; margin: 10px 0; font-weight: bold; }
.event-form li label { display: inline; font-weight: normal; }
.event-form li { display: inline; list-style: none; padding: 0px; margin: 0 10px 0 0; }
.event-form input[type="submit"] { display: block; float: right; }

#event-table tr form { visibility: hidden; }
#event-table tr:hover form { visibility: visible; }

#event-table th { text-align: left; font-weight: bold; } 
label[for="id_device"], label[for="id_active"] { display: none; }
#id_device, #id_active { display: none; }
